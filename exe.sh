numof_category=2
fillrate=0.1
weight=0.2
imagesize=362
numof_point=100000
numof_ite=200000
save_dir="./data"
pretraining_epochs=5
finetuning_epochs=10
instance_num=1
arch=resnet50

howto_draw='gaussian_gray'#"{point, patch, gaussian}_{gray, color}"
function_type="nonlinear"#"linear"or"nonlinear"

## Parameter search
python3 fractal_renderer/ifs_search.py --rate=${fillrate} --category=${numof_category} --numof_point=${numof_point} --save_dir=${save_dir} --function_type=${function_type}

## Create FractalDB
python3 fractal_renderer/make_fractaldb.py \
    --load_root=${save_dir}'/rate'${fillrate}'_category'${numof_category}'_'${function_type}'/csv' --save_root=${save_dir}'/'${function_type}'-'${howto_draw}'-fractal'${numof_category} \
    --image_size_x=${imagesize} --image_size_y=${imagesize} --iteration=${numof_ite} --draw_type=${howto_draw} \
    --weight_csv='./fractal_renderer/weights/weights_'${weight}'.csv' --instance=${instance_num}

# FractalDB Pre-training
python3 pretraining/main.py --path2traindb=${save_dir}'/'${function_type}'-'${howto_draw}'-Fractal'${numof_category} --dataset=${function_type}'-'${howto_draw}'-fractal'${numof_category} --numof_classes=${numof_category} --usenet=${arch} --epochs=${pretraining_epochs} --batch_size=32

# Fine-tuning
python3 finetuning/main.py --path2db='./data/CIFAR10' --path2weight='./data/weight' --dataset=${function_type}'-'${howto_draw}'-fractal'${numof_category} --ft_dataset='CIFAR10' --numof_pretrained_classes=${numof_category} --usenet=${arch} --epochs=${finetuning_epochs}
