/**
 * Auto Update JD Cookie pt_key

1. Save code to scripts/pt_key.js.
2. Add surge module with the follow config.

#!name=pt_key
#!desc=Auto update pt_key
#!system=ios
#!arguments=qinglongHost:http://192.168.1.2:5700,clientId:"",clientSecret:""

[Script]
http-response ^https?:\/\/api\.m\.jd\.com\/client\.action\?functionId=(wareBusiness|serverConfig|basicConfig) requires-body=1,script-path=scripts/pt_key.js, argument=qinglongHost={{{qinglongHost}}}&clientId={{{clientId}}}&clientSecret={{{clientSecret}}}

[MITM]
hostname = %APPEND% api.m.jd.com
*/

// 参数处理
let arg;
if (typeof $argument != 'undefined') {
    arg = Object.fromEntries($argument.split('&').map(item => item.split('=')));
} else {
    arg = {};
}

let qinglongHost = arg.qinglongHost;
let clientId = arg.clientId;
let clientSecret = arg.clientSecret;

console.log("qinglongHost = " + qinglongHost)

if (!qinglongHost || !clientId || !clientSecret) {
    console.log("Config surge module argument.");
    $done();
}

// 公共变量
let qinglongToken = "";
let qinglongEnvId = 0;

// 获取 Cookie
var CV = $request.headers["Cookie"] || $request.headers["cookie"];
var jdCookie = CV.match(/pt_pin=.+?;/) + CV.match(/pt_key=.+?;/);

(async function () {
    // 获取 qinglong Token
    await getQinglongToken();

    if (!qinglongToken) {
        console.log('Can not get qinglong token.');
        $done();
        return;
    }

    // 获取 JD_COOKIE 的 envId
    await getQinglongEnvId();
    if (!qinglongEnvId) {
        console.log('Can not get JD_COOKIE env id.');
        $done();
        return;
    }

    await Promise.all([
        // 更新 jd_cookie 值
        updateQinglongEnvValue(),
        // 更新 jd_cookie 状态
        updateQinglongEnvStatus()
    ]);

    // 关闭模块，自需要执行一次
    await $httpAPI("POST", "v1/modules", { ["pt_key"]: false }, () => $done());
    $notification.post("pt_key", "", "Update success!");
    $done();
})();

function getQinglongToken() {
    return new Promise(async (resolve) => {
        $httpClient.get(
            qinglongHost +
            "/open/auth/token?client_id=" +
            clientId +
            "&client_secret=" +
            clientSecret,
            function (error, response, data) {
                try {
                    if (error) {
                        throw new Error(error);
                        return;
                    }

                    const body = JSON.parse(data);
                    if (body.code == 200) {
                        qinglongToken = body.data.token;
                        // console.log(qinglongToken);
                        resolve(true);
                    } else {
                        throw new Error('get qinglong token error.');
                    }
                } catch (e) {
                    console.log(`\nerror: ${e.message}`);
                } finally {
                    resolve();
                }
            }
        );
    });
}

function getQinglongEnvId() {
    return new Promise(async (resolve) => {
        $httpClient.get(
            {
                url: qinglongHost + "/open/envs",
                headers: {
                    Authorization: "Bearer " + qinglongToken,
                    "Content-Type": "application/json"
                }
            },
            function (error, response, data) {
                try {
                    if (error) {
                        throw new Error(error);
                        return;
                    }

                    const body = JSON.parse(data);
                    if (body.code == 200 && body.data.length >= 1) {
                        let jdCookieEnv = body.data.filter(t => t.name == "JD_COOKIE").pop();
                        if (jdCookieEnv) {
                            qinglongEnvId = jdCookieEnv.id;
                            // console.log(qinglongEnvId);
                            resolve(true);
                        }
                    } else {
                        throw new Error('get qinglong evn id error.');
                    }
                } catch (e) {
                    console.log(`\nerror: ${e.message}`);
                } finally {
                    resolve();
                }
            }
        );
    });
}

function updateQinglongEnvValue() {
    return new Promise(async (resolve) => {
        $httpClient.put(
            {
                url: qinglongHost + "/open/envs",
                headers: {
                    Authorization: "Bearer " + qinglongToken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: qinglongEnvId, name: "JD_COOKIE", value: jdCookie })
            },
            function (error, response, data) {
                // console.log(data);
                resolve(true);
            }
        );
    });
}

function updateQinglongEnvStatus() {
    return new Promise(async (resolve) => {
        $httpClient.put(
            {
                url: qinglongHost + "/open/envs/enable",
                headers: {
                    Authorization: "Bearer " + qinglongToken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify([qinglongEnvId])
            },
            function (error, response, data) {
                // console.log(data);
                resolve(true);
            }
        );
    });
}
