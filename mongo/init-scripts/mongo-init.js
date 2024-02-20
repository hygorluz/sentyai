print('Start #################################################################');
const db = db.getSiblingDB('sentyai');

db.createCollection( "sentiments");

db.sentiments.createIndex(
    {"message" : 1},
    {"name": "message", "background": true, "unique" : true}
);

db.sentiments.createIndex(
    {"sentiment_updated_at" : -1},
    {"name": "updated_at", "background": true, "unique" : false}
);

db.sentiments.createIndex(
    {"message" : 1, "sentiment_updated_at" : -1, },
    {"name": "message_sentiment_updated_at", "background": true, "unique" : false}
);
print('END #################################################################');
