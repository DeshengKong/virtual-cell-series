# Episode 1 · What Is a Virtual Cell?

> Status: draft v0.3 (2026-11-09), adapted from the final Chinese script (not a word-for-word translation); revised after freshman + Feynman/fidelity reviews
> Expected length ~6.5 min (≈1,050 words); duration is flexible
> One question only: **What exactly does a virtual cell try to predict?**
> Core insight: **Knowing what a cell looks like right now is not enough to predict what happens when you change one of its genes — you also need the rules inside.**
> Three new terms only: virtual cell, state, perturbation
> 〔Bracketed notes〕 are visual cues, not read aloud.

---

## 1. The opening question

〔Dark background; a cell outline fades in. A few medicine bottles appear beside it.〕

Imagine you're sick, and your doctor has several drugs to choose from.

The doctor looks at clinical trial results, and sometimes at a genetic test. But for one particular person, very often the only way to know is to try.

〔The bottles move toward the cell one by one; small bars inside the cell rise and fall.〕

What if we could first let a "virtual cell" inside a computer react to each drug, and see in advance what would happen? That is what a virtual cell is trying to do.

Today, virtual cells can already predict some of the changes in certain lab experiments. But they are still far from giving reliable answers for every kind of cell and every drug. And whether a drug actually works once it's inside a human body is a different question altogether.

## 2. What it actually predicts

〔A machine appears in the center: two inputs on the left, one output on the right.〕

The whole idea of a virtual cell fits in one sentence:

〔Each item lights up in turn〕

Input: the state the cell is in right now, plus what you do to it.
Output: what it turns into.

"What you do to it" could be adding a drug, or switching off a gene, or sending the cell a signal from outside, such as a hormone. Labs have special tools for switching off genes, and we'll get to them later. Scientists call each of these a "perturbation".

So what is a "state"? That's easier to show than to explain, so let's build a cell and look.

## 3. A toy cell: running a prediction ourselves

〔Dark background. Three dots appear, labeled A, B, C, each with a bar beneath it.〕

This is a toy cell we designed ourselves. It has only three genes: A, B and C.

You may have learned in school that a gene is like a blueprint. In this toy, each gene is the blueprint for one kind of protein, and that protein changes how much of another gene's protein gets made. From here on, "A" means gene A and its protein, and the same for B and C. The three bars below show how much of each protein there is.

〔A blue arrow appears from A to B〕Protein A pushes up the making of B.
〔A blue arrow appears from B to C〕Protein B pushes up the making of C.
〔A red-orange "⊣" appears from C to A〕And protein C, in turn, holds back the making of A. This T-shaped symbol means "holds back".

〔The three bars wobble a few times, then settle at the same height, labeled "1".〕

The cell keeps making these proteins, and it also keeps breaking them down. Left alone, production and breakdown balance out, and the three bars settle at a fixed height. We'll call that height 1.

〔A bracket labeled "state" appears next to the bars.〕

The heights of these three bars are this cell's "state" right now. Scientists call it the cell state.

Now let's apply a perturbation: we switch off gene B. The cell stops making protein B, and the protein B already there slowly breaks down to 0.

〔B's bar starts falling; dot B turns gray.〕

Take a guess first: we didn't touch A. What happens to A?

〔Pause for 2 seconds; a "?" appears above A.〕

〔The animation is driven by toycell simulation data: B falls first, then C falls, and A rises last.〕

With B gone, C loses its push and slowly drops to 0. Real cells wouldn't drop this cleanly. That's a simplification in our toy.

And C had been holding A back all along. In our toy's rules, C at its normal level cuts A's production in half. Now that nothing holds it back, A is made at full speed. Breakdown keeps pace with how much A there is, so twice the production means A rises to twice its old level, and stays there.

〔A's bar stops at 2; the "⊣" fades away.〕

Notice this result: we never touched A, and yet A changed.

Now think about it: before we switched off B, all three bars read 1. Looking only at those three numbers, could you have guessed that A would double? No. What really decides the outcome is the set of rules between the bars: who pushes whom, and who holds back whom. So knowing what a cell looks like right now isn't enough. You also need to know the rules inside.

〔Back to the machine: the three original bars fly into the first input, "switch off B" flies into the second, and new bars come out of the output. Three arrows light up inside the machine.〕

Back to the machine from the start. The original heights of the three bars are "the cell's state right now". Switching off B is "what you did". And once things calm down, wherever the bars settle is the "new state" the machine gives back. And what's inside the machine is exactly those few rules.

That "half" and that "twice" weren't pulled out of the air. They come straight out of the rules we set, and in later episodes you'll work them out yourself, with nothing more than arithmetic.

## 4. It's like a weather forecast — except in three ways

〔Cut to weather: today's cloud map → tomorrow's cloud map.〕

This is a bit like a weather forecast: put in today's weather, compute tomorrow's. But there are three differences, and they're exactly the hardest parts of this field.

〔The screen splits into three columns that light up in turn.〕

First: a weather forecast mainly predicts how the atmosphere changes on its own. A virtual cell also has to answer: if we deliberately poke the cell, what happens?

Second: we can watch the sky all day, but it's very hard to watch a cell "from start to finish". To measure thousands of genes in one cell at once, the most common method, called single-cell sequencing, first breaks the cell open, so after one measurement, that cell is gone. Newer methods that don't break the cell do exist, but they're still far from recording continuously, like a video. And single-cell sequencing mostly reads RNA, a working copy of the blueprint, not the proteins in our bars. So even the reading we do get is one step removed.

So what can we do? The same thing you did with controlled experiments in school: take two groups of similar cells, leave one alone, perturb the other, and compare the two groups. But "similar" doesn't mean "identical", and that brings new problems of its own, which we'll come back to in a later episode.

Third, and most fundamental: weather forecasting rests on well-established physics equations, even though the details still need approximations. In a cell, many of the rules themselves are still unknown. The three rules in our toy were set by us. A real human cell has nearly twenty thousand genes that code for proteins, and for most of them, who pushes whom and who holds back whom is still unknown.

〔The number "3" grows into "nearly 20,000", then turns into a network where most links are dashed lines and question marks.〕

## 5. Two roads

〔The machine appears again in the center, with two roads branching beneath it.〕

If we don't know the rules, how do we build this machine? Broadly, there are two approaches.

One is what we did with the toy cell: first work out the rules one by one, write them as math, and let the computer calculate.

〔On the left road, a blackboard full of equations; on the right, thousands of "untouched / perturbed" cell-group pairs flowing past like cards.〕

The other: don't write the rules first. Instead, collect lots of the comparison data we just described: one group left alone and one group perturbed, thousands of times over. Then let artificial intelligence find the rules in those differences on its own.

〔A balance appears at the top: "model prediction" on one side, "experimental result" on the other.〕

Whichever road we take, the machine we build has to be tested against real experiments. And in actual research, the two roads are often combined.

## 6. Summary and a question for you

〔Four boxes light up around the machine: state, perturbation, how to build the machine, how to test it. Not read aloud.〕

Every episode from here on will take on one part of this machine.

〔The screen comes back to the one sentence.〕

If you remember one sentence from this episode, make it this:
**A virtual cell takes a cell's state and what you do to it, and predicts what the cell turns into.**

〔The toy cell appears again; this time C turns gray.〕

Here's a question to think about: what if we switch off C instead of B? What happens to A and B? Will B rise to exactly 2, just like A?
We'll reveal the answer at the start of the next episode.

---

## Internal notes (not read aloud)

Same model and numbers as the Chinese script (`script.md`, "内部备注"): toycell v0.1; KO B → A 2, B 0, C 0; KO C → A 2, B 1.6, C 0.

Adaptation choices:
- 图纸 → "blueprint"; 复印件 → "working copy of the blueprint" (not "photocopy"; fixed in `docs/concepts.yml`).
- 推动 / 压住 → "pushes (up)" and "holds back", used consistently; on screen: "pushes" / "holds back".
- 开足马力 → "full power"; 打平 → "balance out".
- "高中" → "in school" (curricula differ by country).
- Section duration notes removed; English pace differs.
- Deliberate small departures from the Chinese (from the English freshman test): "C at its normal level cuts A's production in half" is stated when explaining half power (the Chinese leaves it to the later "calculated from rules" line); "we can watch the sky all day" makes the weather contrast explicit; "such as a hormone" makes the outside signal concrete; "with nothing more than arithmetic".
- Check in TTS: letter A must be read "ay" (e.g. "What happens to A?").
