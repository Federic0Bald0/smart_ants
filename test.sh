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

# python main.py 50 300 100 100 30 4 10 30 0 30 0 > test_results/base &
# python main.py 50 300 100 100 30 4 10 30 0 30 0 > test_results/base_2
# python main.py 50 300 100 100 30 4 10 30 100 30 0 > test_results/base_100_delay_2
python main.py 50 300 100 100 30 3 30 50 0 30 0 > test_results/3_d_p &
python main.py 50 300 100 100 30 4 30 50 0 30 0 > test_results/4_d_p &
python main.py 50 300 100 100 30 6 30 50 0 30 0 > test_results/6_d_p &
python main.py 50 300 100 100 50 4 10 30 0 30 0 > test_results/50_d_n &
python main.py 50 300 100 100 100 4 10 30 0 30 0 > test_results/100_d_n &
python main.py 50 300 100 100 30 4 10 30 0 10 0 > test_results/10_turns &
python main.py 50 300 100 100 30 4 10 30 0 20 0 > test_results/20_turns &
python main.py 50 100 100 100 30 4 10 30 0 30 0 > test_results/100_food &
python main.py 50 400 100 100 30 4 10 30 0 30 0 > test_results/400_food &
python main.py 50 300 200 100 30 4 10 30 0 30 0 > test_results/200_colony &
python main.py 50 300 100 200 30 4 10 30 0 30 0 > test_results/200_energy 
# python main.py 50 200 40 50 5 5 30 30 0 30 0 > test_results/5_dangers
# python main.py 50 200 40 50 35 5 30 30 0 30 0 > test_results/35_dangers
# python main.py 50 200 40 100 20 2 30 30 0 30 0 > test_results/2_d_pow
# python main.py 50 200 40 100 20 10 30 30 0 30 0 > test_results/10_d_pow
# python main.py 50 200 40 100 20 5 20 30 0 30 0 > test_results/20_sel_ration
# python main.py 50 200 40 100 20 5 50 30 0 30 0 > test_results/50_sel_ration
# python main.py 50 200 40 100 20 5 30 20 0 30 0 > test_results/20_mut
# python main.py 50 200 40 100 20 5 30 50 0 30 0 > test_results/50_mut
# python main.py 50 200 40 100 20 5 30 30 20 30 0 > test_results/20_d_app
# python main.py 50 200 40 100 20 5 30 30 40 30 0 > test_results/40_d_app
# python main.py 50 300 100 100 30 4 10 30 0 30 0 > test_results/mutation_50 &
# python main.py 50 300 100 100 30 4 10 30 0 30 0 > test_results/selection_40 
cd test_results 
rm -rf ./*.png
cd ..
python plot_test_results.py



