import argparse
import cowsay as cowsay


parser = argparse.ArgumentParser()

presets = "bdgpstwy"
for flag in "bdgpstwy":
    parser.add_argument(f"-{flag}", action="store_true")

parser.add_argument("-n", action="store_true")
parser.add_argument("-W", type=int, default=40)
parser.add_argument("-e", type=str)
parser.add_argument("-T", type=str)
parser.add_argument("-f", type=str)
parser.add_argument("-l", action="store_true")
parser.add_argument("message")

args = parser.parse_args()

preset = None
for p in presets:
    if args.__dict__.get(p):
        preset = p
        break

if args.l:
    print(cowsay.list_cows())
else:
    print(
        cowsay.cowsay(
            message=args.message,
            cow=args.f,
            preset=preset,
            eyes=args.e,
            tongue=args.T,
            width=args.W,
            wrap_text=args.n,
        )
    )
