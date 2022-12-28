python fractal_renderer/ifs_search.py --rate=0.1 --category=10 --numof_point=100000  --save_dir='./data' --function_type=nonlinear

python fractal_renderer/make_fractaldb.py \
    --load_root='./data/rate0.1_cat10_linear/csv_rate0.1_category10'
    --save_root='./data/Nonlinear-Fractal10\'
    --draw_type="point_gray"