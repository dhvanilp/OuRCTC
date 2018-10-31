var express = require('express');
var router = express.Router();

router.post('/text', function (req, res, next) {
    console.log(req.body);
    res.render('index', {title: 'PRCTC: Search'});
});

router.post('/map', function (req, res, next) {
    // console.log(req.body);
    res.send(req.body)
    // res.render('index', {title: 'PRCTC: Search'});
});

module.exports = router;
