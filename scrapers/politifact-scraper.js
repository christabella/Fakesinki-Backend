var Promise        = require('bluebird')
,   fs             = require('fs')
,   Xray           = require("x-ray")
,   xray           = new Xray().delay('5s', '10s')
,   baseUrl = "http://www.politifact.com/truth-o-meter/statements/?page=";

// Currently baseUrl has 640 pages
// var pageNumbers = Array.apply(null, Array(640)).map(function (_, i) {return i + 1;});


console.log("xraying first page");

xray("http://www.politifact.com/truth-o-meter/statements", 'div.statement', [{
    ruling_text: 'p.quote',
    ruling: '.meter img@alt', // equivalent to $('div.statement').find('.meter img').attr("alt")
    statement: 'p.statement__text a',
    statement_link: 'p.statement__text a.link@href',
    time: 'span.article__meta',
    source: 'div.statement__source a',
    source_image: 'div.mugshot img@src'
  }])
  (function(err, result){
      if (err) {
        console.log('Error reading from page');
      } else {
        console.log('finished one page')
      }
  })
  .paginate('.step-links__next@href')
  .write("politifact_data/statements.json");
