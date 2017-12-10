
'use strict'
const Log = exports

var path = require('path')
var log4js = require('log4js');


exports.configure = function() {
    log4js.configure(path.join(__dirname, "log4js.json"));    
}


exports.logger = function(name) {
    var dateFileLog = log4js.getLogger(name);
    // dateFileLog.setLevel(log4js.levels.INFO);
    return dateFileLog;
}

exports.logger2 = function(name) {
    var dateFileLog = log4js.getLogger();
    dateFileLog.level = 'info';
    // dateFileLog.setLevel(log4js.levels.INFO);
    return dateFileLog;
}

exports.useLog = function() {
    return log4js.connectLogger(log4js.getLogger("app"), {level: log4js.levels.INFO});
} 