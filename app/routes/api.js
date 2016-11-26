var express = require('express');
var router = express.Router();

var pg = require('pg');

pg.defaults.ssl = true;

/* GET first row. */
router.get('/getFirst', function(req, res, next) {
    pg.connect(process.env.DATABASE_URL, function(err, client) {
      if (err) throw err;
      console.log('Connected to postgres! Getting schemas...');

      client
        .query('SELECT * FROM statements LIMIT 1;', function(err, result) {
            if (err) {
                console.error(err); res.send("Error " + err); 
            } else { 
                res.send(result.rows); 
            }
        })
    });
});

/* GET random row. */
router.get('/getRandom', function(req, res, next) {
    pg.connect(process.env.DATABASE_URL, function(err, client) {
      if (err) throw err;
      console.log('Connected to postgres! Getting schemas...');

      client
        .query('SELECT * FROM statements OFFSET floor(random()*10000) LIMIT 1;', function(err, result) {
            if (err) {
                console.error(err); res.send("Error " + err); 
            } else { 
                res.send(result.rows); 
            }
        })
    });
});



module.exports = router;
