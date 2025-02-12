# Copyright (c) 2020-present, Francesco Croce
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import math
import numpy as np

import torch
import torch.nn.functional as F

from libs.utilities.losses import Dice_metric


class SquareAttack():
    """
    Square Attack
    https://arxiv.org/abs/1912.00049

    :param predict:       forward pass function
    :param n_restarts:    number of random restarts
    :param n_queries:     max number of queries (each restart)
    :param eps:           bound on the norm of perturbations
    :param seed:          random seed for the starting point
    :param p_init:        parameter to control size of squares
    :param loss:          loss function optimized ('margin', 'ce' supported)
    :param resc_schedule  adapt schedule of p to n_queries
    """

    def __init__(
            self,
            predict,
            dice_thresh,
            n_queries=5000,
            eps=None,
            p_init=.8,
            n_restarts=1,
            seed=0,
            verbose=False,
            loss='margin',
            resc_schedule=True,
            device=None):
        """
        Square Attack implementation in PyTorch
        """

        self.predict = predict
        self.n_queries = n_queries
        self.eps = eps
        self.p_init = p_init
        self.n_restarts = n_restarts
        self.seed = seed
        self.verbose = verbose
        self.loss = loss
        self.rescale_schedule = resc_schedule
        self.device = device
        # Dice loss
        self.dice_thresh = dice_thresh
        self.dice = Dice_metric(eps=1e-5)

    def margin_and_loss(self, x, y):
        """
        :param y:        correct labels
        """

        logits = self.predict(x)
        dice = self.dice(logits.detach(), y)
        return dice, dice # margin, margin

    def init_hyperparam(self, x):
        assert self.eps is not None
        assert self.loss in ['ce', 'margin']

        if self.device is None:
            self.device = x.device
        self.orig_dim = list(x.shape[1:])
        self.ndims = len(self.orig_dim)
        if self.seed is None:
            self.seed = time.time()

    def random_target_classes(self, y_pred, n_classes):
        y = torch.zeros_like(y_pred)
        for counter in range(y_pred.shape[0]):
            lst = list(range(n_classes))
            lst.remove(y_pred[counter])
            t = self.random_int(0, len(lst))
            y[counter] = lst[t]

        return y.long().to(self.device)

    def check_shape(self, x):
        return x if len(x.shape) == (self.ndims + 1) else x.unsqueeze(0)

    def random_choice(self, shape):
        t = 2 * torch.rand(shape).to(self.device) - 1
        return torch.sign(t)

    def random_int(self, low=0, high=1, shape=[1]):
        t = low + (high - low) * torch.rand(shape).to(self.device)
        return t.long()

    def normalize(self, x):
        t = x.abs().view(x.shape[0], -1).max(1)[0]
        return x / (t.view(-1, *([1] * self.ndims)) + 1e-12)

    def eta_rectangles(self, x, y):
        delta = torch.zeros([x, y]).to(self.device)
        x_c, y_c = x // 2 + 1, y // 2 + 1

        counter2 = [x_c - 1, y_c - 1]
        for counter in range(0, max(x_c, y_c)):
            delta[
                max(counter2[0], 0):min(counter2[0] + (2*counter + 1), x),
                max(0, counter2[1]):min(counter2[1] + (2*counter + 1), y)
                ] += 1.0/(torch.Tensor([counter + 1]).view(1, 1).to(
                    self.device) ** 2)
            counter2[0] -= 1
            counter2[1] -= 1

        delta /= (delta ** 2).sum(dim=(0, 1), keepdim=True).sqrt()
        return delta

    def eta(self, s):
        delta = torch.zeros([s, s]).to(self.device)
        delta[:s // 2] = self.eta_rectangles(s // 2, s)
        delta[s // 2:] = -1. * self.eta_rectangles(s - s // 2, s)
        delta /= (delta ** 2).sum(dim=(0, 1), keepdim=True).sqrt()
        if torch.rand([1]) > 0.5:
            delta = delta.permute([1, 0])

        return delta

    def p_selection(self, it):
        """ schedule to decrease the parameter p """

        if self.rescale_schedule:
            it = int(it / self.n_queries * 10000)

        if 10 < it <= 50:
            p = self.p_init / 2
        elif 50 < it <= 200:
            p = self.p_init / 4
        elif 200 < it <= 500:
            p = self.p_init / 8
        elif 500 < it <= 1000:
            p = self.p_init / 16
        elif 1000 < it <= 2000:
            p = self.p_init / 32
        elif 2000 < it <= 4000:
            p = self.p_init / 64
        elif 4000 < it <= 6000:
            p = self.p_init / 128
        elif 6000 < it <= 8000:
            p = self.p_init / 256
        elif 8000 < it:
            p = self.p_init / 512
        else:
            p = self.p_init
        return p

    def attack_single_run(self, x, y):
        with torch.no_grad():
            c, d, h, w = x.shape[1:]
            n_features = c * d * h * w
            n_ex_total = x.shape[0]
            root_cube = lambda x: x**(1./3.) if 0 <= x else -(-x)**(1./3.)

            x_best = torch.clamp(x + self.eps * self.random_choice(
                [x.shape[0], c, 1, h, w]), 0., 1.)
            margin_min, loss_min = self.margin_and_loss(x_best, y)
            n_queries = torch.ones(x.shape[0]).to(self.device)
            for i_iter in range(self.n_queries):
                if i_iter % 100 == 0:
                    print(i_iter)
                idx_to_fool = (margin_min > self.dice_thresh).nonzero().squeeze()
                x_curr = self.check_shape(x[idx_to_fool])
                x_best_curr = self.check_shape(x_best[idx_to_fool])
                y_curr = y[idx_to_fool]
                if len(y_curr.shape) == 3:
                    y_curr = y_curr.unsqueeze(0)
                margin_min_curr = margin_min[idx_to_fool]
                loss_min_curr = loss_min[idx_to_fool]

                p = self.p_selection(i_iter)
                s = max(int(round(root_cube(p * n_features / c))), 1)
                vd = self.random_int(0, d - s)
                vh = self.random_int(0, h - s)
                vw = self.random_int(0, w - s)
                new_deltas = torch.zeros([c, d, h, w]).to(self.device)
                new_deltas[
                    :, vd:vd + s, vh:vh + s, vw:vw + s
                    ] = 2. * self.eps * self.random_choice([c, 1, 1, 1])

                x_new = x_best_curr + new_deltas
                x_new = torch.min(torch.max(x_new, x_curr - self.eps),
                                  x_curr + self.eps)
                x_new = torch.clamp(x_new, 0., 1.)
                x_new = self.check_shape(x_new)

                margin, loss = self.margin_and_loss(x_new, y_curr)
                # update loss if new loss is better
                idx_improved = (loss < loss_min_curr).half()

                loss_min[idx_to_fool] = idx_improved * loss + (
                    1. - idx_improved) * loss_min_curr

                # update margin and x_best if new loss is better
                # or misclassification
                idx_miscl = (margin < self.dice_thresh).half()
                idx_improved = torch.max(idx_improved, idx_miscl)

                margin_min[idx_to_fool] = idx_improved * margin + (
                    1. - idx_improved) * margin_min_curr
                idx_improved = idx_improved.reshape(
                    [-1, *[1]*len(x.shape[:-1])])
                x_best[idx_to_fool] = idx_improved * x_new + (
                    1. - idx_improved) * x_best_curr
                n_queries[idx_to_fool] += 1.

                curr_dice, _ = self.margin_and_loss(x_best, y)
                ind_succ = (self.dice(
                    self.predict(x_best).detach(),
                    y) < self.dice_thresh).nonzero().squeeze()
                if self.verbose and ind_succ.numel() != 0:
                    print(
                        '{}'.format(i_iter + 1),
                        '- success rate={}/{} ({:.2%})'.format(
                            ind_succ.numel(), n_ex_total,
                            float(ind_succ.numel()) / n_ex_total),
                        '- avg # queries={:.1f}'.format(
                            n_queries[ind_succ].mean().item()),
                        '- med # queries={:.1f}'.format(
                            n_queries[ind_succ].median().item()),
                        '- loss={:.3f}'.format(loss_min.mean()))

                if ind_succ.numel() == n_ex_total:
                    break

        return n_queries, x_best

    def perturb(self, x, y=None):
        """
        :param x:           clean images
        :param y:           clean labels, if None we use the predicted labels
        """

        self.init_hyperparam(x)

        adv = x.clone()
        if y is None:  # haven't studied this case, for now
            with torch.no_grad():
                output = self.predict(x)
                y_pred = output.max(1)[1]
                y = y_pred.detach().clone().long().to(self.device)
        else:
            y = y.detach().clone().long().to(self.device)

        acc = self.dice(self.predict(x).detach(), y) > self.dice_thresh

        startt = time.time()

        torch.random.manual_seed(self.seed)
        torch.cuda.random.manual_seed(self.seed)

        for counter in range(self.n_restarts):
            ind_to_fool = acc.nonzero().squeeze()
            if len(ind_to_fool.shape) == 0:
                ind_to_fool = ind_to_fool.unsqueeze(0)
            if ind_to_fool.numel() != 0:
                x_to_fool = x[ind_to_fool].clone()
                y_to_fool = y[ind_to_fool].clone()

                _, adv_curr = self.attack_single_run(x_to_fool, y_to_fool)
                acc_curr = self.dice(self.predict(adv_curr).detach(), y_to_fool) > self.dice_thresh
                ind_curr = (acc_curr == 0).nonzero().squeeze()

                acc[ind_to_fool[ind_curr]] = 0
                adv[ind_to_fool[ind_curr]] = adv_curr[ind_curr].clone()
                if self.verbose:
                    print('restart {} - robust accuracy: {:.2%}'.format(
                        counter, acc.float().mean()),
                        '- cum. time: {:.1f} s'.format(
                        time.time() - startt))

        return adv_curr
