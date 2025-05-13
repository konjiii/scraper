import { StopwordsEn, TokenizerEn, StemmerEn } from "@nlpjs/lang-en";

const tokenizer = new TokenizerEn();
const stemmer = new StemmerEn();
stemmer.stopwords = new StopwordsEn();

const sent =
  "I'm a Very, very running fasteR upset man: this is why. lol ; ; \" , .";

// const sent = "Who is your DEVELOPER";

console.log(stemmer.tokenizeAndStem(sent, false));

const data = new Map();

data.set("test", 5);
data.set("test2", 2);

console.log(data.get("test") + 1);
console.log(data.get("test2") + 1);
console.log((data.get("test3") || 0) + 1);
console.log(data.keys());
