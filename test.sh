# Standard inference
# python main.py --task TASK_ID --gpu GPU_IDs --batch BATCH_SIZE --name OUTPUT_DIR --test

# AutoAttack
# python main.py --task TASK_ID --gpu GPU_IDs --batch BATCH_SIZE --name OUTPUT_DIR --test --adv

# 1
task_list='
2
3
4
5
6
7
8
9
'
for task in $task_list; do
    # python main.py --task $task --gpu 0 --batch 1 --name at_output --test
    # python main.py --task $task --gpu 0 --batch 1 --name at_output --test --adv

    # python main.py --task $task --gpu 0 --batch 1 --name pgd_output --test
    # python main.py --task $task --gpu 0 --batch 1 --name pgd_output --test --adv

    # python main.py --task $task --gpu 0 --batch 1 --name FREE_out --test
    # python main.py --task $task --gpu 0 --batch 1 --name FREE_out --test --adv

    # python main.py --task $task --gpu 0 --batch 1 --name DEAT_out --test
    # python main.py --task $task --gpu 0 --batch 1 --name DEAT_out --test --adv

    python main.py --task $task --gpu 0 --batch 1 --name PGD_out --test
    python main.py --task $task --gpu 0 --batch 1 --name PGD_out --test --adv
done