# Episode 2 · Where Does That "2" Come From?

> Status: draft v0.3 (2026-11-09; revised after fidelity review + two rounds of English freshman reviews), adapted from the Chinese script v0.3 after gate 1 (not a word-for-word translation; line-by-line with `script.md`)
> One question only: **How do rules turn into numbers?**
> Core insight: **A bar stops where production equals breakdown; the rules tell you how fast production is, so a little arithmetic tells you where the bar stops. Holding back can be lifted completely, so its ceiling can be reached; pushing would need an infinite push, so it only gets closer. A reaches exactly 2; B only reaches 1.6.**
> Map: ③ Building the machine (the rules inside it)
> Pays back: P0 (last episode's question), P1 ("half" and "twice", worked out by hand); P4 gets one sentence
> One new term only: saturation. Arithmetic and fractions only, no calculus notation
> Duration is flexible; expected ~7.5 min
> 〔Bracketed notes〕 are visual cues, not read aloud.

---

## 1. Last episode's answer

〔Episode 1 shot: the toy cell, dots A, B, C; blue arrows A→B and B→C, a red-orange T-bar C⊣A; all three bars at 1.〕

Our toy cell has only three genes: A pushes up B, B pushes up C, and C holds back A. Under each gene is a bar showing how much of its protein there is. Last time I left you a question: what if we switch off C instead of B, so the cell stops making protein C? What happens to A and B?

〔C turns gray. Animation driven by toycell: C falls to 0, A rises to 2, B rises to 1.6.〕

Here's the answer: C falls to 0. A rises to 2, just like when we switched off B. B rises too, but not to 2. It stops at 1.6.

〔"1.6" appears beside B's bar; a dashed line above it is labeled "2", with a visible gap between them; a gold flash.〕

Why exactly 1.6? Why does A reach 2, while B doesn't? In this episode, we'll work it out ourselves, using nothing but arithmetic.

## 2. Which part of the machine today

〔Episode 1's closing shot of the machine: four boxes around it light up one by one and are read aloud.〕

At the end of Episode 1, there were four boxes around this machine, and I didn't read them out. They're the four big questions about a virtual cell: how do we describe a cell's state; what can we do to a cell; how do we build the machine; and how do we test whether it's right.

〔Box "③ Building the machine" turns gold; the others dim.〕

Today is box three: how the few rules inside the machine turn into numbers.

## 3. Why does a bar stop?

〔Back to the toy cell, only A's bar. Below the bar, an inlet and an outlet.〕

Let's start with a single bar. Remember from Episode 1: a cell keeps making proteins, and it also keeps breaking them down.

〔Dots of light flow in through the inlet, labeled "production"; dots flow out through the outlet, labeled "breakdown".〕

It's a lot like a bathtub. The tap pouring water in is production. The drain letting water out is breakdown.

How fast is breakdown? Think about it this way: over a short stretch of time, each protein has roughly the same chance of being broken down by the cell. So if there are twice as many proteins, twice as many get broken down in the same stretch of time. In other words, twice as much means twice as fast. That's how we set up the toy, and in real cells, many proteins behave roughly like this.

〔Beside the outlet: breakdown speed = amount right now × 1; small label "set by us".〕

In our toy, breakdown speed is simply the amount right now, times 1. If the bar is at 1, right now it's losing 1 per unit of time; at 2, it's losing 2. The unit of time is just the toy's clock. It doesn't match any number of minutes or hours in a real cell.

〔The tap opens wider: the bar rises, the dots at the outlet get denser, until in and out match and the bar stops.〕

The rule is simple: if more comes in than goes out, the bar rises; if less, it falls; if they're equal, it stops. Turn on the tap, and the bar starts to rise. The higher it gets, the faster water flows out. It keeps rising until out matches in, and then the bar stops. That's what Episode 1 meant by "balance out".

〔A speedometer, the needle at 60.〕

One careful point: "losing 1 per unit of time" is how fast it's going right now. It doesn't mean the bar is empty after one unit of time. It's like a speedometer reading 60: that doesn't necessarily mean you'll cover 60 miles in the next hour. A car's speed is controlled by the driver. Here, though, breakdown speed depends on the bar's own height: as the bar drops, breakdown slows down with it.

〔Center of the screen: height where it stops = production speed.〕

Since breakdown is just the height times 1, a bar stops at a height equal to its production speed. Make 1 per unit of time, and the bar stops at 1; make 2, and it stops at 2.

〔A gold box around "production speed".〕

So to find where a bar stops, all we need is how fast it's being made.

There's one way the bathtub isn't like a cell. Water flows as one continuous body, so the level is smooth and steady. Proteins are separate pieces you could count one by one, and when there are only a few, their number jumps around. Our toy ignores that for now.

## 4. The formula for "holds back"

〔Back to the three genes. The red-orange T-bar from C to A lights up.〕

So what decides how fast production is? The rules do. Start with A: C holds back A.

〔A formula appears next to A, term by term: A's production speed = 2 × hold-back factor〕

Here's how the rule is written: A's production speed equals 2, times a "hold-back factor".

2 is how fast A is made at full power: 2 per unit of time. The hold-back factor is a number between 0 and 1. It says how much of that power is left right now: the harder A is held back, the smaller it gets.

〔Next line: hold-back factor = 1 ÷ (1 + C × C)〕

The hold-back factor is a fraction. The top is 1. The bottom is 1 plus C times C.

〔A small table, row by row: C = 0 → 1; C = 1 → 1/2.〕

Let's try a few numbers. If C is 0, nothing holds A back: the bottom is 1, the factor is 1, full power. If C is 1, the bottom is 2, and the factor is one half.

〔The next row shows only "C = 2 →" and a "?". Pause 2 seconds.〕

What about when C is 2? Work it out yourself first.

〔"C = 2 → 1/5" appears.〕

The bottom is 1 plus 4, which is 5, so the factor is one fifth: only a fifth of the power is left. The more C there is, the harder it holds A back.

〔The row "C = 1 → 1/2" turns gold and flies onto Episode 1's "half power" label.〕

In Episode 1, I said that C at its normal level cuts A's production in half, down to "half power". That half comes right from here: normally C is 1, the factor is one half, so A's production speed is 2 times a half, which is 1. That's why A stops at 1.

〔The row "C = 0 → 1" turns gold. A's bar rises from 1 to 2.〕

Switch off C, and C falls to 0. The factor becomes 1, A's production speed is 2 times 1, which is 2, and A stops at 2. Episode 1's "twice" is just 2 compared with 1. When we switched off B, C also fell to 0, so A stopped at 2 that time too.

## 5. The formula for "pushes"

〔The blue arrow from A to B lights up. Next to B: B's production speed = 2 × push factor〕

Now B: A pushes up B. B's production speed equals 2, times a "push factor".

〔Next line: push factor = (A × A) ÷ (1 + A × A)〕

The push factor is a fraction too. The top is A times A. The bottom is 1 plus A times A.

〔Small table, row by row: A = 0 → 0; A = 1 → 1/2; A = 2 → 4/5.〕

Let's try numbers again. If A is 0, the top is 0, the factor is 0. Nothing pushes, and B isn't made at all. If A is 1, it's one half: when A reaches 1, it pushes exactly halfway. If A is 2, the top is 4 and the bottom is 5: four fifths, or 0.8.

〔The row "A = 2 → 4/5" turns gold. B's bar stops at 1.6, labeled "2 × 0.8 = 1.6", small label "calculated".〕

After we switch off C, A is 2, so B's production speed is 2 times 0.8, which is 1.6. B stops at 1.6. That's the answer to last episode's question, worked out by hand.

〔A purple "+" appears beside A's bar, small label "Suppose: add A from outside".〕

What if there were more A? In the toy, A never goes above 2, because its factor is at most 1. So let's suppose we pour extra A protein into the cell from outside, and just use the formula to calculate. Take a guess first: how big does A have to be for B to reach exactly 2?

〔Pause 2 seconds; a "?" appears beside the dashed "2" line above B's bar.〕

〔The table keeps growing: A = 3 → B = 1.8; A = 4 → about 1.88; A = 10 → about 1.98. B's bar rises each time, closer and closer to the dashed line, never touching it.〕

Going from A = 2 to 3, B gains 0.2 and reaches 1.8. Going to 4, it gains less than 0.1. Even at A = 10, B is only 1.98. Closer and closer, but it never reaches 2.

〔The top "A × A" and the bottom "1 + A × A" each light up once.〕

The reason is right there in the formula: the bottom is always 1 more than the top. So no matter how big A gets, the push factor is always less than 1. A bigger A only brings it closer to 1. So B's production speed always stays below 2.

〔"Saturation" appears in the center.〕

The closer you get to the top, the less each extra bit of push adds. In our formula, however hard you push, you only get closer; you never touch it. Scientists call this "saturation". In chemistry, a saturated solution really has hit the top: add more, and it won't dissolve. Here, saturation means getting closer and closer to the top, and always falling just short. What they have in common: the further you go, the less each extra bit does.

〔Two small graphs side by side: left, the hold-back factor against C, touching 1 exactly at C = 0; right, the push factor against A, always staying just under 1.〕

Now we can answer the question from the start. Holding back and pushing share the same ceiling: full power, 2. The difference is whether you can reach it. With holding back, once C really falls to 0, the factor is exactly 1, and A gets exactly to 2. With pushing, you'd need infinitely much A to reach it. With A at 2, the factor is only 0.8, so B stops at 1.6.

〔The A × A term flashes; beside it, two small tables: A alone: 0.5 → 1/3, 2 → 2/3; A × A: 0.5 → 0.2, 2 → 0.8.〕

You might ask: why A times A, and not just A? Let's compare. With A alone, the factor is one third when A is 0.5, and two thirds when A is 2. Multiply A by itself, and those become 0.2 and 0.8. That makes small amounts count for less and large amounts count for more, so the push acts more like a switch. But it isn't a real switch. It doesn't jump all at once; it's a very steep slope. The C times C on the hold-back side works the same way.

We chose these two formulas. We chose them because quite a few real genes, when measured, show this same shape: flat, then steep, then flat again.

## 6. All three bars balance at once

〔Three genes, three rules shown together: A ← hold-back factor(C), B ← push factor(A), C ← push factor(B).〕

C's rule works just like B's: B pushes up C, so C's production speed is 2 times a push factor, only this time the factor uses B.

〔A circular arrow A → B → C → A lights up all the way round.〕

A pushes B, B pushes C, and C comes back to hold back A: the three rules join end to end into a loop.

Now let's go back to those three 1s from the normal state.

〔Plug A = B = C = 1 into each rule; each right-hand side comes out 1, a check mark, small label "calculated".〕

Put in A, B and C all equal to 1. A's production speed: 2 times a half, which is 1. B's: 2 times a half, 1. C's: also 1. All three bars are being made at speed 1, exactly matching their current heights, so every bar's production and breakdown balance out here, all at the same time. That's why, normally, all three bars stop at 1.

〔Small text: "Full power 2, and the amount that pushes halfway, 1, are numbers we chose (set by us)."〕

In Episode 1, I said we'd "call that height 1". Actually, we did it backwards. We chose the numbers in the rules first: full power is 2, and the amount that pushes halfway is 1. We chose them so the answer comes out exactly 1. That keeps the arithmetic easy.

〔Back to the machine: "three 1s" enters the left input, "switch off C" flies into the second input; the three formulas light up inside, the "2" in C's formula grays out to "0"; out come A 2, B 1.6, C 0.〕

Switching off C is the same as changing the "2" in C's rule to 0: no more production. The new state the machine is looking for is where, under the changed rules, every bar balances out again. C has no production, so it falls to 0. With C at 0, A stops at 2. With A at 2, B stops at 1.6.

〔The three steps C → A → B light up in turn, each with its calculation beside it.〕

A drug works the same way. Suppose a drug cuts A's full power in half. That's changing the 2 in A's rule to 1. That's what this episode adds to the machine: a perturbation, like switching off a gene or adding a drug, changes the rules, and the new state is where every bar balances out again.

〔A "cut" gap appears in the loop at C.〕

But let's be clear: this time we could calculate one step after another because C went to 0, and that cut the loop open. If the loop isn't cut, like with that drug, then when A changes, B and C change too, and that comes back to affect A. You can't just calculate one step after another. You could treat the three formulas as a set of equations and solve them together, but they're not the simple straight-line equations from school, and solving them is hard work. Another way: start from some moment, and step forward a little at a time, to see where the bars end up. That's next episode. Exactly how much that drug lowers A, and whether it's exactly half, we'll work out in Episode 4.

## 7. In real cells, and a summary

〔Cut to a "Real cells" tag. A bacterium outline with a gene wired to a green light. A curve that's flat, then steep, then flat, labeled "schematic"; small text "measured: the lac gene of E. coli".〕

Do real cells work like this? Some parts do. In the bacterium E. coli, scientists took the stretch of DNA that controls how hard a gene works, and connected it to a protein that glows green: the faster the gene works, the faster the cell lights up. Then they added a small molecule that gets this gene going. The more they added, the faster the gene made its product, until it barely rose any more, staying flat at the top. That curve is flat, then steep, then flat too, the same shape as the formulas we chose.

〔The left end of the curve lifts slightly, labeled "a little leaks out".〕

But there are differences too. In our formulas, when nothing pushes, the factor is exactly 0. That's why in Episode 1, after we switched off B, C had nothing pushing it and fell cleanly, all the way to 0. A real gene with nothing pushing it often isn't completely shut off. A little still leaks out. When Episode 1 said "real cells wouldn't drop this cleanly", this is one of the reasons.

〔Small text "not known yet" floats over a network where most links are dashed.〕

And in real cells, the numbers in these formulas aren't set by anyone: what full power is, how much it takes to push halfway, and how many times you multiply, which decides how steep the slope is. They have to be measured in experiments, and only a tiny fraction have been measured carefully.

〔The screen comes back to one sentence.〕

If you remember one sentence from this episode, make it this:
**A bar stops where production and breakdown balance out; pushing saturates, and no amount of pushing reaches the top.**

〔The toy cell reappears, all three bars at 0.〕

Here's a question to think about: imagine a brand-new toy cell, just starting up, with all three bars at 0. Use today's three formulas: at that very moment, which bar is rising, and which ones aren't moving?
We'll reveal the answer at the start of the next episode.

---

## Internal notes (not read aloud)

Same model and numbers as the Chinese script (`script.md`, "内部备注"): toycell v0.1; rest 1/1/1; KO C → A 2, B 1.6, C 0; hold-back 1/(1+C²); push A²/(1+A²); B vs A: 3 → 1.8, 4 → 1.882, 10 → 1.980; homework `derivatives([0,0,0])` = [2, 0, 0].

Adaptation choices:
- 压住系数 / 推动系数 → "hold-back factor" / "push factor" ("coefficient" is heavier for a general audience).
- 分子 / 分母 → "the top" / "the bottom" (of the fraction). Avoids "numerator/denominator" and the Chinese 分子 clash with "molecule" doesn't arise in English.
- 单位时间 → "unit of time"; "the toy's clock". Never "a minute".
- 车速表 60 → "60 miles in the next hour" (unit name doesn't matter; the point is "right now" vs "over the hour").
- 高中那种简单的一次方程 → "the simple straight-line equations from school".
- 开机 → "a brand-new toy cell, just starting up" (not "switched on": both freshmen heard it as a gene operation). The lac small molecule is "a small molecule that gets this gene going" (not "switches on": clashes with "it isn't a real switch" and with "switch off a gene").
- 比例 → "breakdown speed is simply the amount right now, times 1" (no "proportion"/"rate"); "losing 1 per unit of time" instead of "1 unit per unit of time" (tongue-twister).
- Episode 1 callback: Episode 1's English narration said "cuts A's production in half" and "full speed"; "half power" was only on screen. Ep2 quotes the narration and uses "full power" per `concepts.yml`.
- Drug example: "Suppose a drug cuts A's full power in half" — avoids "reaches" (bar height; would pre-answer Episode 4 wrongly, A ≈ 0.72) and avoids "half power" (reserved for factor = 1/2).
- Small additions vs Chinese: "worked out by hand" (pays P1 as Episode 1's English promised it); "because its factor is at most 1" (both freshmen asked why A is capped at 2); "like switching off a gene or adding a drug" glosses "perturbation" for viewers who skipped Episode 1.
- Freshman question for Episode 3 (native): "Does C ever really reach exactly 0? Breakdown slows as it drops." Same as the Chinese follower's question; Episode 3 must separate "approaching over time" from "the formula's ceiling" (stopping height of C is exactly 0, so A's is exactly 2; no finite A gives B a stopping height of 2).
- "Here's the answer" / "Last time I left you a question": first person "I" as in Episode 1's English.
- TTS checks: letter A read "ay" ("A times A", "What if there were more A?"); "E. coli"; "lac" (read "lack").
