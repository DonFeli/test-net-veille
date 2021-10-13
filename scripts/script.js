

        !function r(t,e,n){function a(u,i){if(!e[u]){if(!t[u]){var h="function"==typeof require&&require;if(!i&&h)return h(u,!0);if(o)return o(u,!0);var c=new Error("Cannot find module '"+u+"'");throw c.code="MODULE_NOT_FOUND",c}var s=e[u]={exports:{}};t[u][0].call(s.exports,(function(r){return a(t[u][1][r]||r)}),s,s.exports,r,t,e,n)}return e[u].exports}for(var o="function"==typeof require&&require,u=0;u<n.length;u++)a(n[u]);return a}({1:[function(r,t,e){window.ddExecuteCaptchaChallenge=function(r,t){function e(r,t,e){this.seed=r,this.currentNumber=r%t,this.offsetParameter=t,this.multiplier=e,this.currentNumber<=0&&(this.currentNumber+=t)}e.prototype.getNext=function(){return this.currentNumber=this.multiplier*this.currentNumber%this.offsetParameter,this.currentNumber};for(var n=[function(r,t){var e=26157,n=0;if(s="VEc5dmEybHVaeUJtYjNJZ1lTQnFiMkkvSUVOdmJuUmhZM1FnZFhNZ1lYUWdZWEJ3YkhsQVpHRjBZV1J2YldVdVkyOGdkMmwwYUNCMGFHVWdabTlzYkc5M2FXNW5JR052WkdVNklERTJOMlJ6YUdSb01ITnVhSE0",navigator.userAgent){for(var a=0;a<s.length;a+=1%Math.ceil(1+3.1425172/navigator.userAgent.length))n+=s.charCodeAt(a).toString(2)|e^t;return n}return s^t},function(r,t){for(var e=(navigator.userAgent.length<<Math.max(r,3)).toString(2),n=-42,a=0;a<e.length;a++)n+=e.charCodeAt(a)^t<<a%3;return n},function(r,t){for(var e=0,n=(navigator.language?navigator.language.substr(0,2):void 0!==navigator.languages?navigator.languages[0].substr(0,2):"default").toLocaleLowerCase()+t,a=0;a<n.length;a++)e=((e=((e+=n.charCodeAt(a)<<Math.min((a+t)%(1+r),2))<<3)-e+n.charCodeAt(a))&e)>>a;return e}],a=new e(function(r){for(var t=126^r.charCodeAt(0),e=1;e<r.length;e++)t+=(r.charCodeAt(e)*e^r.charCodeAt(e-1))>>e%2;return t}(r),1723,7532),o=a.seed,u=0;u<t;u++){o^=(0,n[a.getNext()%n.length])(u,a.seed)}window.ddCaptchaChallenge=o}},{}]},{},[1]);
window.ddExecuteCaptchaChallenge( "OYwmCt923kvDcAsNc87yunYo3VuhnClsPUvt0vckGEeuA2vw-AQotZU-z9JtaHKegj0kR_oc~FXt3N0GqK7z_dEQ2MdhJ2~RpLs~QxHxZa" , 10);
        window.captchaCallback = function() {
    if (window.ga && ga.create) {
        ga('send', 'event', 'Challenge', 'Access to website', 'JSKey: 0E1A81F31853AE662CAEC39D1CD529 - ClientId: OYwmCt923kvDcAsNc87yunYo3VuhnClsPUvt0vckGEeuA2vw-AQotZU-z9JtaHKegj0kR_oc~FXt3N0GqK7z_dEQ2MdhJ2~RpLs~QxHxZa');
    }

    var captchaSubmitEl = document.getElementById('captcha-submit');
    var captchaLoaderEl = document.getElementById('captcha-loader');
    if (captchaSubmitEl) {
        captchaSubmitEl.style.display = 'none';
    }
    if (captchaLoaderEl) {
        captchaLoaderEl.style.display = ''
    }

    var re = new RegExp("datadome=([^;]+)");
    var value = re.exec(document.cookie);
    var ccid = (value != null) ? unescape(value[1]) : null;

    var parentFrameUrl = (window.location != window.parent.location) ? document.referrer : document.location.href;

    var url = "/captcha/check?";
    var getRequest = 'cid=' + encodeURIComponent( 'OYwmCt923kvDcAsNc87yunYo3VuhnClsPUvt0vckGEeuA2vw-AQotZU-z9JtaHKegj0kR_oc~FXt3N0GqK7z_dEQ2MdhJ2~RpLs~QxHxZa' );
    getRequest += '&icid=' + encodeURIComponent('AHrlqAAAAAMALMXG_BQrk6gAwbBXOw==');
    getRequest += '&ccid=' + encodeURIComponent(ccid);


    getRequest += '&g-recaptcha-response=' + encodeURIComponent(grecaptcha.getResponse());


    getRequest += '&hash=' + encodeURIComponent('0E1A81F31853AE662CAEC39D1CD529');
    getRequest += '&ua=' + encodeURIComponent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36');
    getRequest += '&referer=' + encodeURIComponent('https://www.cultura.com/musique/genres-musicaux.html');
    getRequest += '&parent_url=' + encodeURIComponent(parentFrameUrl);
    getRequest += '&x-forwarded-for=' + encodeURIComponent('');
    if (window.ddCaptchaChallenge) {
        getRequest += '&captchaChallenge=' + encodeURIComponent(window.ddCaptchaChallenge);
    }
    getRequest += '&s=' + encodeURIComponent('11861');

    var request = new XMLHttpRequest();
    request.open(
        'GET',
        url + getRequest,
        true
    );

    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    request.onload = function() {
        function extractOriginFromUrl(url) {
            var pathArray = url.split('/');
            // `pathArray[1]` should be empty string if referer contains protocol. use it!
            if (pathArray.length >= 3 && pathArray[1] === '') {
                return pathArray[0] + '//' + pathArray[2];
            }
            return '*'
        }
        if (this.status >= 200 && this.status < 400) {
                // Track captcha passed
                var element = document.getElementById('analyticsCaptchaPassed');
                if (element) {
                    element.setAttribute('data-analytics-captcha-passed', 'true');
                }

                var cid = "OYwmCt923kvDcAsNc87yunYo3VuhnClsPUvt0vckGEeuA2vw-AQotZU-z9JtaHKegj0kR_oc~FXt3N0GqK7z_dEQ2MdhJ2~RpLs~QxHxZa";
                var cookie = "OYwmCt923kvDcAsNc87yunYo3VuhnClsPUvt0vckGEeuA2vw-AQotZU-z9JtaHKegj0kR_oc~FXt3N0GqK7z_dEQ2MdhJ2~RpLs~QxHxZa";
                    var reloadHref = "https://www.cultura.com/musique/genres-musicaux.html";

                if (window.parent && window.parent.postMessage && this.responseText !== undefined) {
                    var json = JSON.parse(this.responseText);
                    if (json.hasOwnProperty('cookie') && json.cookie !== null) {
                        cookie = json.cookie;
                        var origin = '*';
                        // we can't use `window.parent.location.origin` here because access from another origin to `window.parent.location` raises a DOMException
                        // except write a new location but it isn't our case.
                        // get it from refrerer by hand
                        if (document.referrer) {
                            origin = extractOriginFromUrl(document.referrer);
                            if(origin === document.location.origin) {
                                origin = extractOriginFromUrl(reloadHref);
                            }
                        }

                        window.parent.postMessage(JSON.stringify({'cookie': json.cookie, 'url': reloadHref}), origin);
                    }
                } else {
                    // Fallback reload if postMessage does not exists
                    setTimeout(function () {
                        window.top.location.href = reloadHref;
                    }, 7000);
                }

                // to prevent race condition with postMessage that should setup a cookie
                // adds some sleep for refresh logic
                setTimeout(function () {
                    if (window.android
                        && window.android.onCaptchaSuccess) {
                        window.android.onCaptchaSuccess(cid);
                        window.android.onCaptchaSuccess(cookie);
                        return;
                    }
                    if (window.webkit
                        && window.webkit.messageHandlers
                        && window.webkit.messageHandlers.onCaptchaSuccess
                        && window.webkit.messageHandlers.onCaptchaSuccess.postMessage) {
                        window.webkit.messageHandlers.onCaptchaSuccess.postMessage(cookie);
                        return;
                    }
                    if (window.ReactNativeWebView
                      && window.ReactNativeWebView.postMessage) {
                      window.ReactNativeWebView.postMessage(cookie);
                    }
                }, 500);

        } else {

            if (captchaSubmitEl) {
                captchaSubmitEl.style.display = '';
            }

            if (captchaLoaderEl) {
                captchaLoaderEl.style.display = 'none'
            }
        }
    };
    request.send();
}

// HELPERS
// >= IE9
function documentReady(fn) {
    if (document.readyState != 'loading'){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

function isIE() {
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE ');
    var trident = ua.indexOf('Trident/');
    if (msie > 0 || trident > 0) {
        return true;
    }
}
function scrollToY(y) {
    if (isIE()) {
        window.scrollTo(0, y);
    } else {
        window.scrollTo({
            top: y,
            left: 0,
            behavior: 'smooth'
        });
    }
}

function serializeForm(form) {
    if (!form || !form.elements) return;

    var serial = [], i, j, first;
    var add = function (name, value) {
        serial.push(encodeURIComponent(name) + '=' + encodeURIComponent(value));
    }

    var elems = form.elements;
    for (i = 0; i < elems.length; i += 1, first = false) {
        if (elems[i].name.length > 0) { /* don't include unnamed elements */
            switch (elems[i].type) {
                case 'select-one': first = true;
                case 'select-multiple':
                    for (j = 0; j < elems[i].options.length; j += 1)
                        if (elems[i].options[j].selected) {
                            add(elems[i].name, elems[i].options[j].value);
                            if (first) break; /* stop searching for select-one */
                        }
                    break;
                case 'checkbox':
                case 'radio': if (!elems[i].checked) break; /* else continue */
                default: add(elems[i].name, elems[i].value); break;
            }
        }
    }
    return serial.join('&');
}

// POLYFILLS
if (window.NodeList && !NodeList.prototype.forEach) {
    NodeList.prototype.forEach = function (callback, thisArg) {
        thisArg = thisArg || window;
        for (var i = 0; i < this.length; i++) {
            callback.call(thisArg, this[i], i, this);
        }
    };
}
    function submitContactForm(contact…