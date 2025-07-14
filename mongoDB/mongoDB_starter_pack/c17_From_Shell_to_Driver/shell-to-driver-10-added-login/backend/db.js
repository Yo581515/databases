const mongodb = require('mongodb');

const MongoClient = mongodb.MongoClient;

//const mongoDbUrl =
//'mongodb+srv://maximilian:hqG9VedJmagiKhKo@cluster0-ntrwp.mongodb.net/shop?retryWrites=true';

const username = process.env.MONGO_USERNAME;
const password = process.env.MONGO_PASSWORD;
const cluster = process.env.MONGO_CLUSTER;
const dbname = process.env.MONGO_DBNAME;

const mongoDbUrl = `mongodb+srv://${username}:${password}@${cluster}/${dbname}?retryWrites=true&w=majority`;


let _db;

const initDb = callback => {
  if (_db) {
    console.log('Database is already initialized!');
    return callback(null, _db);
  }
  MongoClient.connect(mongoDbUrl)
    .then(client => {
      _db = client;
      callback(null, _db);
    })
    .catch(err => {
      callback(err);
    });
};

const getDb = () => {
  if (!_db) {
    throw Error('Database not initialzed');
  }
  return _db;
};

module.exports = {
  initDb,
  getDb
};
