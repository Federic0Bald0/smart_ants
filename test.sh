# 'Usage: python main.py \
#         <environment size> \
#         <food amount> \
#         <colony size> \
#         <ants energy higher than zero> \
#         <number of dangers> \
#         <dangers base power> \
#         <selected ratio> \
#         <mutation prob> \
#         <danger appereance> \
#         <turns> \
#         <display> '

python main.py 50 50 40 100 20 5 30 30 0 30 0 > test_results/base
python main.py 50 50 40 100 20 5 30 30 0 20 0 > test_results/20_turns
python main.py 50 50 40 100 20 5 30 30 0 40 0 > test_results/40_turns
python main.py 50 20 40 100 20 5 30 30 0 30 0 > test_results/20_food
python main.py 50 80 40 100 20 5 30 30 0 30 0 > test_results/80_food
python main.py 50 50 70 100 20 5 30 30 0 30 0 > test_results/70_colony
python main.py 50 50 40 50 20 5 30 30 0 30 0 > test_results/50_energy
python main.py 50 50 40 150 20 5 30 30 0 30 0 > test_results/150_energy
python main.py 50 50 40 50 5 5 30 30 0 30 0 > test_results/5_dangers
python main.py 50 50 40 50 35 5 30 30 0 30 0 > test_results/35_dangers
python main.py 50 50 40 100 20 2 30 30 0 30 0 > test_results/2_d_pow
python main.py 50 50 40 100 20 10 30 30 0 30 0 > test_results/10_d_pow
python main.py 50 50 40 100 20 5 20 30 0 30 0 > test_results/20_sel_ration
python main.py 50 50 40 100 20 5 50 30 0 30 0 > test_results/50_sel_ration
python main.py 50 50 40 100 20 5 30 20 0 30 0 > test_results/20_mut
python main.py 50 50 40 100 20 5 30 50 0 30 0 > test_results/50_mut
python main.py 50 50 40 100 20 5 30 30 20 30 0 > test_results/20_d_app
python main.py 50 50 40 100 20 5 30 30 40 30 0 > test_results/40_d_app
python plot_test_results.py



