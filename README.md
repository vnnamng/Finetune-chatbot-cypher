# Chatbot using ChatGPT on NEO4J AuraDB

This chatbot leverages OpenAI's ChatGPT and NEO4J AuraDB to provide an interactive interface capable of understanding and generating Cypher queries. It is designed to assist users in querying and visualizing graph data stored in a NEO4J database. The chatbot can interpret natural language inputs, convert them into Cypher queries, and display the results, making it easier to interact with complex graph databases.

User target: intended for users who are not familiar with Cypher and Neo4j languages. It aims to help them perform business intelligence and data analysis tasks quickly and efficiently.
 

## How to run:
1. import into .env files these variable
```env
NEO4J_URI= <URI to NEO4J db>
NEO4J_USERNAME= <USERNAME>
NEO4J_PASSWORD= <PASSWORD>

OPENAI_KEY= <OPENAI_KEY>
```

2. `docker build -t chatbot .` 
    > If error, check if docker deamon has been started.
3. `docker run -d -p 8501:8501 --name chatbot-container chatbot`
4. Access the chatbot at port 8501 of localhost: 'http://localhost:8501/'

## Features:
1. Chatbot with knowledge of KG schema and can generate cypher queries
2. Full Graph Visualisation
3. Custom visualisation based on past queries result from chatbot answer.

## Customisation

1. Adjust behaviour and scope and personality in `src/train_cypher.py`
2. Add examples queries to `src/train_utils.py`

## Future Improvements

1. Use langchain to implement LogicalAgent to fix limitaiton of not able to queries multiple level.
2. Improve performance on large scale graph
3. Add semantics queries.

## Contributors:
1. [ Xuan Nam ](https://github.com/vnnamng)
2. [ Amanda ](https://github.com/Apandax): UI/UX and chatbot customisation
3. [ Viscacha ](https://github.com/raven0205): Docker Setup
4. [Zhouyu](https://github.com/tzy815): Sponsor of API Key
5. [Team Weeping Wranglers from NUS DSA3101 AY24/25S1](https://github.com/AY2425S1-DSA3101-Weeping-Wranglers): Source of Neo4J data, ER, Set Up, etc...