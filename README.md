# Artificial Intelligence in Education: Automated Essay Grading
Increasing numbers of high school students are taking AP exams every year.  
In 2022, College Board had $500M in revenue from AP exams. 
![ap exam](https://i.insider.com/655a45b24ca513d8242bf8ab?width=700)  
![image](Picture1.png)
Essay readers are compensated at $30/hour plus travel expenses. Over the course of a week, 1500 teachers grade aproximately 2500 essays each costing College Board $1.8M just in labor. Additionally this greuling schedule raises questions on essay reader fatigue and its impact on the grades assigned.  
By creating an AI essay grader, AP essays could be graded faster, with less potential for score variation due to human factors. 


## Learn more about the Team
Desmond Harvey: [@Desmond-Harvey](https://github.com/Desmond-Harvey)  
Madeline McGaughey: [@maddiemcgoy9](https://github.com/maddiemcgoy9)  
John Mintz: [@jpmintz](https://github.com/jpmintz)  
Morgan Warner: [@MorganTench](https://github.com/MorganTench)  

## About the Paper

This paper introduces a new AI model called DualBERT-Trans-CNN that automatically grades essays by looking at both the overall quality and specific writing traits.  These traits include content, organization, grammar, word choice and many more. Most older systems give just one overall score to an essay, but this model gives detailed feedback by analyzing essays from two angles: the big picture and the smaller details. It uses BERT, a powerful language model, to understand the essay's meaning and structure. Compared to other multi task models, it improved holistic scoring by 2% on the ASAP++ dataset.  When compared to single task models, it improved trait specific scoring by an average of 3.6%.  Overall, the combination of overall essay understanding and trait analysis help the model give more accurate feedback.


## References


[Automated Essay Grading](https://onlinelibrary.wiley.com/doi/10.4218/etrij.2023-0324): article that led us to choosing this topic. It provides background information on different NLP (Natural Language Processing) and CNN (Convolutional Neural Network) models that could be used to automate essay grading.

[ProPublica: College Board](https://projects.propublica.org/nonprofits/organizations/131623965)

[Total Registration: College Board](https://www.totalregistration.net/AP-Exam-Registration-Service/Follow-The-Money-History-of-College-Board-Finances.php)

[AP essay grading timeframe](https://morganparkacademy.wordpress.com/2015/07/08/behind-the-scenes-at-the-ap-exam-or-how-to-grade-2500-essays-in-one-week/)
