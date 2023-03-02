# python dat_main.py --AT --task 2 --gpu 0 --batch 3 --name DEAT_out

# python dat_main.py --task 1 --gpu 0 --batch 3 --name DEAT_out --AT

# python dat_main.py --task 1 --gpu 0 --batch 3 --name DEAT_out --AT
# python main.py --task 1 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 1 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 2 --gpu 0 --batch 2 --name DEAT_out --AT
# python main.py --task 2 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 2 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 3 --gpu 0 --batch 4 --name DEAT_out --AT
# python main.py --task 3 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 3 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 4 --gpu 0 --batch 22 --name DEAT_out --AT
# python main.py --task 4 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 4 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 5 --gpu 0 --batch 13 --name DEAT_out --AT
# python main.py --task 5 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 5 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 6 --gpu 0 --batch 2 --name DEAT_out --AT
# python main.py --task 6 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 6 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 7 --gpu 0 --batch 4 --name DEAT_out --AT
# python main.py --task 7 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 7 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 8 --gpu 0 --batch 16 --name DEAT_out --AT
# python main.py --task 8 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 8 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 9 --gpu 0 --batch 5 --name DEAT_out --AT
# python main.py --task 9 --gpu 0 --batch 1 --name DEAT_out --test
# python main.py --task 9 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python dat_main.py --task 10 --gpu 0 --batch 3 --name DEAT_out --AT


# python main.py --task 2 --gpu 0 --batch 2 --name FREE_out --AT

# python main.py --task 3 --gpu 0 --batch 2 --name FREE_out --AT

# python main.py --task 4 --gpu 0 --batch 22 --name FREE_out --AT

# python main.py --task 5 --gpu 0 --batch 13 --name FREE_out --AT

# python main.py --task 6 --gpu 0 --batch 2 --name FREE_out --AT

# python main.py --task 7 --gpu 0 --batch 3 --name FREE_out --AT

# python main.py --task 8 --gpu 0 --batch 5 --name FREE_out --AT

# python main.py --task 9 --gpu 0 --batch 5 --name FREE_out --AT

# python main.py --task 10 --gpu 0 --batch 3 --name FREE_out --AT

# python pgd_main.py --task 2 --gpu 0 --batch 2 --name PGD_out --AT
# python pgd_main.py --task 3 --gpu 0 --batch 2 --name PGD_out --AT
# python pgd_main.py --task 4 --gpu 0 --batch 22 --name PGD_out --AT
# python pgd_main.py --task 5 --gpu 0 --batch 13 --name PGD_out --AT
# python pgd_main.py --task 6 --gpu 0 --batch 2 --name PGD_out --AT
# python pgd_main.py --task 7 --gpu 0 --batch 3 --name PGD_out --AT
# python pgd_main.py --task 8 --gpu 0 --batch 5 --name PGD_out --AT
# python pgd_main.py --task 9 --gpu 0 --batch 5 --name PGD_out --AT
# python pgd_main.py --task 10 --gpu 0 --batch 3 --name PGD_out --AT

python at_main.py --task 3 --gpu 0  --batch 2 --name DEAT_out_1 --AT --adv_trainer dfree
python at_main.py --task 3 --gpu 0 --batch 1 --name DEAT_out_1 --test
python at_main.py --task 3 --gpu 0 --batch 1 --name DEAT_out_1 --test --adv

python at_main.py --task 3 --gpu 0  --batch 2 --name FREE_out --AT --adv_trainer free
python at_main.py --task 3 --gpu 0 --batch 1 --name FREE_out --test
python at_main.py --task 3 --gpu 0 --batch 1 --name FREE_out --test --adv

python at_main.py --task 4 --gpu 0  --batch 22 --name DEAT_out_1 --AT --adv_trainer dfree
python at_main.py --task 4 --gpu 0 --batch 1 --name DEAT_out_1 --test
python at_main.py --task 4 --gpu 0 --batch 1 --name DEAT_out_1 --test --adv

python at_main.py --task 4 --gpu 0  --batch 22 --name FREE_out --AT --adv_trainer free
python at_main.py --task 4 --gpu 0 --batch 1 --name FREE_out --test
python at_main.py --task 4 --gpu 0 --batch 1 --name FREE_out --test --adv

python at_main.py --task 7 --gpu 0  --batch 3 --name DEAT_out_1 --AT --adv_trainer dfree
python at_main.py --task 7 --gpu 0 --batch 1 --name DEAT_out_1 --test
python at_main.py --task 7 --gpu 0 --batch 1 --name DEAT_out_1 --test --adv


# python at_main.py --task 8 --gpu 0  --batch 5 --name DEAT_out --AT --adv_trainer dfree
# python at_main.py --task 8 --gpu 0 --batch 1 --name DEAT_out --test
# python at_main.py --task 8 --gpu 0 --batch 1 --name DEAT_out --test --adv

# python at_main.py --task 10 --gpu 0  --batch 3 --name DEAT_out --AT --adv_trainer dfree
# python at_main.py --task 10 --gpu 0 --batch 1 --name DEAT_out --test
# python at_main.py --task 10 --gpu 0 --batch 1 --name DEAT_out --test --adv