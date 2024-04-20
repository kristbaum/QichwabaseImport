# Todos:

- [x] Creating items for dialect variants and sources
- [ ] Property proposal
- [x] Create query to extract dataset (different columns for each language sense)
- [ ] Update base script to match workflow

## Creating items for dialect variants and sources
Since we are just importing the Puno Quechua variant, it is described on Wikidata as [Q7260479](https://www.wikidata.org/wiki/Q7260479).

Furthermore, the Runasimi Vocabulary has been described with the [Q125537856](https://www.wikidata.org/wiki/Q125537856)

## Create query to extract dataset (different columns for each language sense)
The query has been described on [Qichwabase](https://qichwa.wikibase.cloud/), it can be found as example on the [Qichwabase's Query Service](https://qichwa.wikibase.cloud/query/).

For obatining the subset of quechua lexemes, the following conditions were met:
* Verbs that are described on Puno Quechua dialect
* Verbs that at least contain a glose

The source is available on [puno_quechua_verbs_with_forms_senses](datasets/puno_quechua_verbs_with_forms_senses.csv)

```
#Puno Quechua Lexical entries
#This is a list of Puno Quechua Lexical entries 
PREFIX qwb: <https://qichwa.wikibase.cloud/entity/>
PREFIX qdp: <https://qichwa.wikibase.cloud/prop/direct/>
PREFIX qp: <https://qichwa.wikibase.cloud/prop/>
PREFIX qps: <https://qichwa.wikibase.cloud/prop/statement/>
PREFIX qpq: <https://qichwa.wikibase.cloud/prop/qualifier/>
PREFIX qpr: <https://qichwa.wikibase.cloud/prop/reference/>
PREFIX qno: <https://qichwa.wikibase.cloud/prop/novalue/>

SELECT ?entry ?lemma ?language ?lex_cat_wikidata ?des_by_source_P1343 
?form1_representation ?form1_spelling_variant 
?sense1_gloss_de ?sense1_gloss_en ?sense1_gloss_es ?sense1_gloss_it
WHERE {
BIND("Q5218" AS ?language) #assigning Q5218 = Quechua Wikidata as the language
BIND(?form_representation AS ?form1_representation) #assigning form_representation of puno quechua to form1_representation 
BIND("qu-x-Q7260479" AS ?form1_spelling_variant) #Assigning the language-code for the form
BIND("Q24905" AS ?lex_cat_wikidata) #Assignning Q24905 = Verb Wikidata as the lexical category
BIND("Q125537856" AS ?des_by_source_P1343) #Assigning Q125537856 = Runasimi Vocabulary as the source
# Wikidata property: described by source = P1343

?entry a ontolex:LexicalEntry; 
       wikibase:lemma ?lemma;
       wikibase:lexicalCategory qwb:Q99 ; #Category Q99 = V.tr Qichwabase
       wikibase:lexicalCategory [rdfs:label ?lexical_category] ;      
       qp:P16 [qps:P16 ?form_representation;
               qpq:P17 qwb:Q116; #Q116 = Cusco-Collao (aiu) Qichwabase
             ]. 
OPTIONAL {
  ?entry ontolex:sense ?sense1_de .
  ?sense1_de skos:definition ?sense1_gloss_de.
  FILTER(LANG(?sense1_gloss_de)="de")
}
OPTIONAL {
  ?entry ontolex:sense ?sense1_en .
  ?sense1_en skos:definition ?sense1_gloss_en.
  FILTER(LANG(?sense1_gloss_en)="en")
}
#OPTIONAL {      # at least contains spanish gloss
  ?entry ontolex:sense ?sense1_es .
  ?sense1_es skos:definition ?sense1_gloss_es.
  FILTER(LANG(?sense1_gloss_es)="es")
#}
OPTIONAL {
  ?entry ontolex:sense ?sense1_it .
  ?sense1_it skos:definition ?sense1_gloss_it.
  FILTER(LANG(?sense1_gloss_it)="it")
}
}
```
[Try it!](https://tinyurl.com/2y8d5lox)

In total there should be about 1650 lexemes to be imported to Wikidata.
