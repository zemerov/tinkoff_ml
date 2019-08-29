import argparse
import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TextGen model learning')
    parser.add_argument('input_text', type=str, help='Text for learning')
    parser.add_argument('--output', type=str, default='default', help='Filename to save model data')

    args = parser.parse_args()

    gen_model = model.TextGen()
    gen_model.fit(args.input_text)
    gen_model.save(args.output)

    print('Success! Model saved to {}'.format(args.output))
