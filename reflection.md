# Reflection: SciComp Ants Project
### Mira Flynn

1. If you had a partner, how was your teaming experience?

I did not have a partner for this project.

2. Previously, you described tasks with deadlines for this project. How did that go? Did you meet the deadlines? Did the project proceed exactly according to your tasks? Were there additional tasks that you did not list? How will you create better tasks and deadlines for the next project?

My task deadlines did not end up holding to my original schedule due to some unexpected factors out of my control. In the future, those exact factors *should* not happen again. As such, I will not be changing my planning process substantially due to this project. Joining the class a few days late also didn't help, as that caused me to squish into a slightly tighter deadline.

However, there is still a big thing to rediscover for the future. If someone is in a situation where external factors are more likely to impact their ability to work, then they should communicate about that and make a plan for what should change to accomodate those conditions. This is why we have DSO, a DSO letter, and why we communicate with our teachers about issues as early and as often as possible.

3. You practiced a computing skill for this project. How did that go? What did you learn? What will you remember for next time?

I practiced writing clean, well documented code for this project. I think that went well, and I'm proud of my output. There were several times where I found bugs not when I wrote them, or noticed their effects, but actually when I went back and intensely commented the code. I'll remember to comment as I go to help me debug and write cleaner code as I went.

4. How did your model compare to your benchmark?

My "benchmark" was essentially having the same broad behavior characteristics, and I think I achieved that. My simulation has chaotic formation, strong highways that get straighter over time, moderate diagonal preference, and just broadly looks about the same.

5. Clearly, and with detail, describe the limitations of your code.

My code is *slow*. I did not optimize it. There are a lot of loops that probably could be numpy functions. There is a *lot* of data being stored per ant. My project already took several minutes to run the simulation, putting it not that much faster than the original paper's vintage computing speed.

6. What are the strengths of your code?

My code is well documented, meaning that others can more easily read, understand, validate, and expand it. Furthermore, it is built in a way that adding and expanding it is easy. The class structure would allow someone to only edit what they want, without substantial changes elsewhere in the model.

7. Was there part of your project that was not captured in your code or presentation? Now’s the time to share with me an area that you spent significant effort on that may not be visible in the other deliverables. Please provide as much detail as possible- if you spent a lot of time on code that didn’t appear in the final repository version, please include with this submission. (I may assign extra credit in this category to offset a lower grade on your Code Submission assignment).

I went into a moderate research tangent about the diagonal behavior of the ants. I didn't do any writing down my search process or what papers I read, and as such, I don't expect extra credit for this. I mainly sat down for a few hours, clicked the "cited by" button on Google Scholar, and opened tabs for anything that looked like it might have an explanation of the diagonal preference. I also spent a while looking at my code and thinking about the diagonals. I didn't come to any major conclusions here, and my only hypothesis is that the additional distance travel of diagonal travel vs. up/down means that the diagonal travel is more likely.

8. Reflect on your presentation. What specific elements of the presentation did you choose to spend time on? What elements of the presentation were successful in communicating to your audience? What elements were less successful? What will you remember for your next presentation?

I didn't expect my presentation to cover much other than those of my classmates, so I didn't focus a ton on my results. I focused more on my diagonal tangent, as I had more to say and I wanted to hear from my classmates about their findings. I spent less time on that tangent than its proportion of my presentation.

I think my communication was a good balance of actual information and me being goofy. I think my lighthearted, not very serious description of the diagonal preference had something to do with the class having a healthy discussion where almost everyone chimed in, and I want to use the same moderately lighthearted approach in the future.