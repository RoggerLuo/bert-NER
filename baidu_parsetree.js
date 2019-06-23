var AipNlpClient = require("baidu-aip-sdk").nlp;


var APP_ID = '15737243'
var API_KEY = 'MmGcFmcpYeG6vEKEBc20K9zP'
var SECRET_KEY = 'fGLes8qGvGrntH1Cx75hnSXoGK5dgmcN'


// 新建一个对象，建议只保存一个对象调用服务接口
var client = new AipNlpClient(APP_ID, API_KEY, SECRET_KEY);


var text = "太阳从哪边升起？";

// 调用依存句法分析
client.depparser(text).then(function(result) {
    console.log(JSON.stringify(result));
}).catch(function(err) {
    // 如果发生网络错误
    console.log(err);
});

// 如果有可选参数
var options = {};
options["mode"] = "1";

// 带参数调用依存句法分析
client.depparser(text, options).then(function(result) {
    console.log(JSON.stringify(result));
}).catch(function(err) {
    // 如果发生网络错误
    console.log(err);
});;





// {"postag":"v","head":0,"word":"升起","id":4,"deprel":"HED"}]
// [{"postag":"n","head":4,"word":"太阳","id":1,"deprel":"SBV"},
// {"postag":"p","head":4,"word":"从","id":2,"deprel":"LOC"},
//         {"postag":"f","head":2,"word":"东边","id":3,"deprel":"POB"},



{"postag":"v","head":0,"word":"升起","id":4,"deprel":"HED"}
[{"postag":"n","head":4,"word":"太阳","id":1,"deprel":"SBV"}
,{"postag":"p","head":4,"word":"从","id":2,"deprel":"LOC"},
        {"postag":"r","head":2,"word":"哪边","id":3,"deprel":"POB"},
,{"postag":"w","head":4,"word":"？","id":5,"deprel":"WP"}]