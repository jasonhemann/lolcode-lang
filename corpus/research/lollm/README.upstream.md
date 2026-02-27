# LOLLM

**A language model trained entirely from LOLCODE.**

```
HAI 1.4
CAN HAS BRAINZ?
I HAS A model ITZ I IZ BRAINZ'Z LOAD YR "brainz.bin" MKAY
I HAS A out ITZ I IZ BRAINZ'Z SPEEK YR model AN YR "An Ceiling Cat maded " AN YR 200 AN YR 0.8 MKAY
VISIBLE "An Ceiling Cat maded " AN out
I IZ BRAINZ'Z KTHXBAI YR model MKAY
KTHXBYE
```

```
An Ceiling Cat maded peps liek cat wat dat r lat an cul teh catz
frinished dan dey sayed, all dey pene. An Ceiling Cat maded teh
Urfs An teh way stuff dat it 2. An teh snaek sayed Ceiling Cat
be awn yu, grly. So he iz al teh moy stuff dat if u hees fiedz
En ak nok at wuz can spenteh 2 walll net din did wuz.
```

## What Is This

A character-level transformer that learns to write LOLCODE programs and LOLCat Bible prose. The entire pipeline — model creation, training, inference — is orchestrated from LOLCODE scripts using the `BRAINZ` library.

The model is a 4-layer transformer with 834K parameters. It was trained on 38KB of LOLspeak text (LOLCODE programs, LOLCat Bible excerpts, and LOLspeak dialogue) for 50,000 steps using the Adam optimizer. Training takes about 90 minutes on a single CPU core.

It has no idea what it's saying, but it's saying it with confidence.

## Sample Output

**Prompt: `An Ceiling Cat maded`** — it writes scripture:
```
An Ceiling Cat maded teh Urfs An teh waterz stuff An all teh
animulz stuff Seaz. An Ceiling Cat maded teh Urfs An teh wuz
An stuff An levz a so. An Ceiling Cat maded dem An all teh
animulz. An Ceiling Cat maded peention iz srsly.
An teh snaek sndz derey started all dat maded.
An teh snaek sayed, DO WANT an dey Fluffy wud efinty din wry.
An Ceiling Cat maded to az rd ewers write ders we
```

**Prompt: `An teh snaek sayed`** — it tells stories:
```
An teh snaek sayed Ceiling Cat be awn yu, grly. So he iz al
teh moy stuff dat if u hees fiedz En ak nok at wuz can
spenteh 2 walll net din did wuz.
```

**Prompt: `HAI 1.4`** — it writes LOLCODE programs:
```
HAI 1.4
    HOW IZ I izprime YR i MKAY, O RLY?
             YA RLY, FOUND YR 1
        OIC
            IM IN YR loooop UPPIN YR i TIL BOTH SAEM i AN 5
        I HAS A maximum ITZ nums'Z SRS 0
    I HAS A minimum ITZ nums'Z SRS 0
```

**Prompt: `MAI KITTEH`** — it preaches:
```
MAI KITTEH ". HAH ITEH TOASTER ING?
Ceiling Cat watches baiting alked. Hey wisuz p wretetetd dem
An I ated it or ez sretly peaine. So Ceiling Cat maded teh
anywaterz dem stufeh day. An Ceiling Cat maded teh Urfs An
teh waterz stuff An I ated out
```

## How It Works

The `BRAINZ` library adds native tensor operations and a transformer model to the [lci](https://github.com/justinmeza/lci) LOLCODE interpreter. No external dependencies — just C and math.

| Component | Details |
|-----------|---------|
| Architecture | 4-layer pre-norm transformer, single-head attention |
| Parameters | 834K (3.2 MB on disk) |
| Vocab | 128 (raw ASCII, character-level) |
| Context window | 64 characters |
| Optimizer | Adam (beta1=0.9, beta2=0.999) |
| Autograd | Eager-mode tape with full backward pass |
| Training data | 38KB of LOLspeak/LOLCODE text |

Under the hood: a from-scratch autograd engine records operations on a global tape during the forward pass, then walks it backward to compute gradients. The Adam optimizer maintains per-parameter momentum estimates. All of this is in pure C — no BLAS, no GPU, no frameworks.

## Usage

### Prerequisites

Build [lci](https://github.com/justinmeza/lci) (BRAINZ support is included by default):

```bash
git clone https://github.com/justinmeza/lci
cd lci
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make
```

### Train

Edit `train.lol` to adjust hyperparameters, then:

```bash
lci train.lol
```

```
STEP 0 LOSS 5.36
STEP 5000 LOSS 1.56
STEP 10000 LOSS 2.77
STEP 15000 LOSS 0.84
...
STEP 45000 LOSS 0.31
DOEN LURNIN
```

### Chat

```bash
lci chat.lol
```

```
BRAINZ READY 4 CHATZ

U> CEILING CAT
BRAINZ> HAZ CHEZBURGER? KTHXBAI! IM IN UR CKIN TER...

U> HAI 1.4
BRAINZ> HOW IZ I izprime YR i MKAY, O RLY? YA RLY, FOUND YR 1...

U> KTHXBYE
```

## Files

| File | What it does |
|------|-------------|
| `train.lol` | Trains a new model from `lolspeak.txt` |
| `chat.lol` | Interactive chat REPL with a trained model |
| `lolspeak.txt` | Training corpus (LOLCODE programs + LOLCat Bible + LOLspeak) |

## The BRAINZ API

```
CAN HAS BRAINZ?                                          BTW import library

I IZ BRAINZ'Z KREEAYT YR "layers=4,hidden=128" MKAY      BTW create model
I IZ BRAINZ'Z STUDEE YR model AN YR text AN YR 0.001 MKAY BTW train step
I IZ BRAINZ'Z SPEEK YR model AN YR prompt AN YR 200 AN YR 0.8 MKAY  BTW generate
I IZ BRAINZ'Z SAVE YR model AN YR "brainz.bin" MKAY       BTW save weights
I IZ BRAINZ'Z LOAD YR "brainz.bin" MKAY                   BTW load weights
I IZ BRAINZ'Z KTHXBAI YR model MKAY                       BTW free memory
```

## Training Corpus

The `lolspeak.txt` corpus is assembled from open sources:

- **LOLCODE programs** — FizzBuzz, Fibonacci, prime checkers, sorting algorithms, 99 bottles, Towers of Hanoi, and more from Rosetta Code and Esolangs
- **LOLCat Bible** — Genesis chapters in LOLspeak from the LOLCat Bible Translation Project
- **LOLspeak dialogue and prose** — conversations, stories, and common phrases in LOLspeak

## License

WTFPL. DO WUT U WANT.
