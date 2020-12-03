var heroScores = {
"Hamlet" : 0,
"Satan" : 0,
"Manfred" : 0,
"Pechorin" : 0,
"Dracula": 0,
"Frankensteins-monster" : 0,
"Heathcliff" : 0,
"Edward" : 0,
"Byron" : 0,
"Nemo" : 0
}
var heroBlurbs = {
  "Hamlet" : "You're not a Byronic hero, quite. You're proto-Byronic, though. You're Hamlet: a tormented soul, you have a complex relationship to self, God, humanity, death, and authority. You're notable too for your quick wits (Harold Bloom thinks you're more intelligent than any possible reader), your morbid sense of humor, and your disturbingly convincing pretense of insanity.",
  "Satan" : "You're Satan. Mind you, though, not the essence of evil. No, you are Milton's Satan, the Satan of paradise lost, an epic hero in the finest mold and an inspiration to many Romantic writers. Blake may be wrong, Milton may not have been of the devil's party, but the authors who read him often were, and given your nobility and eloquence, that's no surprise.",
  "Manfred" : "You are Manfred, hero of Byron's eponymous (possibly autobiographical) closet drama. You are on the more introspective end of the Byronic spectrum: you are consumed with guilt for the death of your True Love, one Astarte, and acutely conscious of your internal contradictions: you combine the best and the worst of humankind (though, it must be confessed, you don't show either too convincingly on the page.)",
  "Pechorin" : "You are Pechorin, Byronic antihero (and self-portrait) of Russian poet, novelist, and Byron-lover Mikhail Lermontov. You have the usual Byronic contradictions: in your case, cynicism and melancholy sensitivity, passion and coldness, impulsivity and piercing insight into yourself and others. Romantically, you're the ultimate player; you feel little attachment to anyone; you have no tolerance for pretense.",
  "Dracula" : "You have fallen from antihero status to straight-up villainy: you're Dracula. You retain a Byronic magnetism, alpha-male-confidence (whether you're male or not), and skill — but as far as the reader can tell, you have, I regret to say, the psychological depth of a mud puddle. But souls aren't terribly helpful in the quest for world domination; you're just fine the way you are, as far as you can tell.",
  "Frankensteins-monster" : "You are Frankenstein's monster. You're famous for other reasons, and you don't have the typical Byronic charisma (though I bet, if you made your story public, you'd find a surprising number of sympathetic souls). Still, you have many core qualities of a Byronic hero: contradictions (you're outwardly monstrous but loving and noble), inner torment, intellect (you learned to read by peeking in windows) and high sensibility. Oh, and you are a raging, vengeful murderer but nonetheless tormented by your crimes.",
  "Heathcliff" : "You are Heathcliff. You're as dark as real Byronic heroes get, and that's...pretty dark. You're a sadistic abuser. You feel no remorse. Still, your redeeming quality is love. Not universal love, not feel-good love, but, well, the love of your life is the center of your life, even after they've left you.",
  "Edward" : "You're...post-Byronic. You've read all those nineteenth-century brooding antiheroes and have strong opinions about them. Still, you carry on the tradition, combining arrogance, a dark past, obsessive love, intense personal magnetism, and profound inner torment. Sure, you've been prettified, you're (in some ways) too good to be true, you might actually literally sparkle, but the lineage is clear. You're Edward Cullen.",
  "Byron": "You're not just Byronic — you're Lord Byron himself! Those tortured, cynical, brooding lady-killers have a real-life source, and yes, you're really like that. You're not faithful in love, but you're incredibly passionate, and your desires transgress cultural boundaries. You're a great poet and a living icon.",
  "Nemo": "You don't appear to have filled out the quiz at all. Try again! Or don't. If you're really a Byronic hero, such trivialities may well be beneath you."
}
var personalityScores = {
"virtue" : 0,
"vice" : 0,
"inner turmoil" : 0,
"magnetism": 0
};
var qNames = ["virtues", "vices", "intolerable", "true-love", "dark-secret", "god", "motivations"]

function updateScores(qName) {
  const choices = document.getElementsByClassName(qName);
  for (let i = 0; i < choices.length; i++) {
      if (choices[i].checked) {
      let heroesStr = choices[i].getAttribute("data-hero");
      let heroes = heroesStr.split(" ")
      for (let i = 0; i < heroes.length; i++) {
        if (heroes[i] in heroScores) {
          heroScores[heroes[i]] += 2;
        }
      }
      let stats = choices[i].getAttribute("data-stats");
      personalityScores["virtue"] += Number(stats[0]);
      personalityScores["vice"] += Number(stats[1]);
      personalityScores["inner turmoil"] += Number(stats[2]);
      personalityScores["magnetism"] += Number(stats[3]);
    }
  }
}
function scoreQuiz() {
  for (let i = 0; i < qNames.length; i++) {
    updateScores(qNames[i]);
  }
  let maxHero = "Nemo";
  for (let hero in heroScores) {
    if (heroScores[hero] >= heroScores[maxHero]) {
      maxHero = hero;
    }
  }
  console.log(maxHero);
  console.log(heroBlurbs[maxHero]);
  document.getElementById("result").innerHTML = heroBlurbs[maxHero];
}
