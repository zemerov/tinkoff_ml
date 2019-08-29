import argparse
import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TextGen model learning')
    parser.add_argument('file', type=str, help='Filename to load the model')
    parser.add_argument('--length', type=int, default=10, help='Phrase length to generate')
    parser.add_argument('--is_rand', type=str, default='false', help='Generation method')
    parser.add_argument('--seed', type=int, default=0, help='Seed')

    args = parser.parse_args()

    gen_model = model.TextGen()
    gen_model.load(args.file)
    print(gen_model.generate(length=args.length, is_rand=(args.is_rand.lower() == 'true'), seed=args.seed))
