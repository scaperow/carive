angular.module('starter.services', ['ngResource'])
    .config(function ($httpProvider) {
        $httpProvider.defaults.headers.post = {
            'Authorization': 'Basic ' + btoa(localStorage.username + ':' + localStorage.password),
            'Access-Control-Allow-Origin': config.domain
        };


        $httpProvider.interceptors.push('HttpInterceptor');
    })

    .factory('Ad', function ($resource, $rootScope, $q) {
        var resource = $resource(config.domain + '/mobile/ads'),
            ads = [];

        return {
            refresh: function () {
                var deferred = $q.defer();
                resource.query(
                    function (data) {
                        ads = _.map(data, function (item) {
                            item.img = config.domain + '/upload/ad/' + item.img;
                            item.href = JSON.parse(item.href);
                            return item;
                        });

                        deferred.resolve(ads);
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject(data);
                    });

                return deferred.promise;
            },
            ads: function () {
                return ads;
            },
            get: function (id) {
                var exists = [];
                _.each(ads, function (ad) {
                    if (ad.id == id) {
                        exists.push(ad);
                    }
                });

                if (exists && exists.length > 0) {
                    return exists[0];
                }

                return null;
            }
        }
    })

    .factory('Products', function ($resource, $rootScope, $q, $filter) {
        var resource = $resource(config.domain + '/mobile/home'),
            products = {};

        return {
            refresh: function () {
                var deferred = $q.defer();
                resource.get(
                    function (result) {
                        products.fruits = _.map(result.f, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                        //products.seckill = _.map(result.m, function (item) {
                        //    item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                        //    item.times = '';
                        //    return item;
                        //});
                        // 按flag排序，正在进行的在顶部
                        //products.seckill = _.sortBy(products.seckill, function (item) {
                        //    var result = 0;
                        //    switch (item.flag) {
                        //    case 0:
                        //        result = 1;
                        //        break;
                        //
                        //    case 1:
                        //        result = 0;
                        //        break;
                        //
                        //    case 2:
                        //        result = 2;
                        //        break;
                        //    }
                        //
                        //    return result;
                        //});
                        products.vegetables = _.map(result.v, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                        products.time = result.time;
                        products.hots = result.k;
                        products.pre_sales = _.map(result.y, function (item) {
                            item.delivery_time = $filter('date')(new Date(item.delivery_time * 1000), 'yyyy-MM-dd');
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                        products.trades = _.map(result.s, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                        products.bargains = _.map(result.t, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                        //products.buying = _.map(result.tg, function (item) {
                        //    item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                        //    return item;
                        //});

                        deferred.resolve(products);
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject(data);
                    });

                return deferred.promise;
            },
            all: function () {
                return products;
            }
        }
    })

    /*
     用户服务
     */
    .factory('User', function ($resource, $q, $rootScope, $http, ShopCar, Favorite) {
        var _current = null,
            valid = false,
            url = config.domain + '/mobile/login',
            resource = $resource(url);

        return {
            resetPassword: function (mobile, password) {
                var resource = $resource(config.domain + '/mobile/resetpassword'),
                    deferred = $q.defer();

                resource.save({
                        password: password,
                        apassword: password,
                        mobile: mobile
                    },
                    function (result) {
                        if (result.flag === 1) {
                            _current = result.msg;
                            valid = true;
                            deferred.resolve({
                                user: _current
                            });
                            localStorage.username = mobile;
                            localStorage.password = hex_md5(password);
                        } else {
                            deferred.reject({
                                message: result.msg
                            });
                        }
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject({
                            message: '网络异常'
                        });
                    });

                return deferred.promise;
            },
            current: function () {
                return _current;
            },
            hasValid: function () {
                return valid;
            },
            valided: function () {
                valid = true;
            },
            setUser: function (user) {
                _current = user;
            },
            loginBackend: function () {
                var name = localStorage['username'],
                    password = localStorage['password'],
                    deferred = $q.defer();


                if (name && password) {
                    this
                        .login(name, password)
                        .then(this.updateProfile)
                        .then(function () {
                            deferred.resolve();
                        })
                        .catch(function (err) {
                            deferred.reject(err);
                        });
                } else {
                    deferred.reject();
                }

                return deferred.promise;
            },
            logout: function () {
                localStorage.clear();
                _current = null;
                valid = false;
            },
            login: function (userName, password) {
                var deferred = $q.defer();
                resource.save({
                        mobile: userName,
                        password: password
                    },
                    function (result) {
                        if (result.flag === 1) {
                            _current = result['msg'];
                            valid = true;

                            localStorage.username = userName;
                            localStorage.password = password;
                            localStorage.with = '';

                            deferred.resolve(result);
                            $rootScope.$broadcast('loginSuccess', result);
                            if (result.hascheckedin) {
                                $rootScope.$broadcast('user:checkInSuccess');
                            }
                        } else {
                            _current = null;
                            valid = false;
                            deferred.reject(result);
                            $rootScope.$broadcast('loginFail', result);
                        }
                    },
                    function (err) {
                        _current = null;
                        valid = false;
                        deferred.reject(err);
                        $rootScope.$broadcast('loginFail', err);
                    });

                return deferred.promise;
            },
            updateProfile: function () {
                var deferred = $q.defer(),
                    resource = $resource(config.domain + '/mobile/profile');

                if (_current) {
                    resource.get({
                            userid: _current.id
                        },
                        function (data) {
                            if (data.flag == 1) {
                                var optionals = data.cars;
                                var gifts = data.gifts;
                                var favorites = data.favorites;

                                $q.all([ShopCar.setOptionals(optionals), ShopCar.setGifts(gifts), Favorite.setFavorites(favorites)])
                                    .then(function () {

                                        $rootScope.$broadcast('user:updateProfileSuccess');
                                        deferred.resolve();
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                        deferred.reject(error);
                                        $rootScope.$broadcast('user:updateProfileFail');
                                    });
                                //                            ShopCar.setOptionals(cars);
                                //                            ShopCar.setGifts(gifts);
                                //                            Favorite.setFavorites(favorites);

                            }
                        },
                        function (data) {
                            console.log(data);
                        });
                } else {
                    $rootScope.$broadcast('user:updateProfileSuccess');
                }
            },
            syncProfile: function () {
                var deferred = $q.defer(),
                    resource = $resource(config.domain + '/mobile/profile');

                if (valid) {
                    resource.get({
                            userid: _current.id
                        },
                        function (data) {
                            if (data.flag == 1) {
                                var optionals = data.cars;
                                var gifts = data.gifts;
                                var favorites = data.favorites;

                                $q.all([ShopCar.merge(_current.id, optionals, gifts), Favorite.merge(_current.id, favorites)])
                                    .then(function () {
                                        deferred.resolve();
                                    })
                                    .catch(function (err) {
                                        console.log(err);
                                        deferred.reject(err);
                                    });
                            }
                        },
                        function (data) {
                            console.log(data);
                        });
                } else {
                    deferred.reject('用户未登录');
                }

                return deferred.promise;
            },
            requestValidationCodeModify: function (mobile) {
                var resource = $resource(config.domain + '/mobile/changepassword/vcode'),
                    deferred = $q.defer();

                resource.get({
                        mobile: mobile
                    },
                    function (result) {

                        if (result.flag === 1) {
                            deferred.resolve({
                                message: result.msg
                            });
                        } else {
                            deferred.reject({
                                message: result.msg
                            });
                        }
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject({
                            message: '网络或服务器异常'
                        });
                    });

                return deferred.promise;
            },
            requestValidationCodeRegister: function (mobile) {
                var resource = $resource(config.domain + '/mobile/vcode'),
                    deferred = $q.defer();

                resource.get({
                        mobile: mobile
                    },
                    function (result) {

                        if (result.flag === 1) {
                            deferred.resolve({
                                message: result.msg
                            });
                        } else {
                            deferred.reject({
                                message: result.msg
                            });
                        }
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject({
                            message: '网络异常'
                        });
                    });

                return deferred.promise;
            },
            requestResetPassword: function (validationCode, mobile) {
                var resoruce = $resource(config.domain + '/mobile/forgotpassword'),
                    deferred = $q.defer();

                resoruce.save({
                        mobile: mobile,
                        vcode: validationCode
                    },
                    function (result) {
                        if (result.flag === 1) {
                            deferred.resolve();
                        } else {
                            deferred.reject({
                                message: result.msg
                            });
                        }
                    },
                    function (error) {
                        deferred.reject({
                            message: '网络异常'
                        });
                    });

                return deferred.promise;
            },
            requestValidationCodeRecovery: function (mobile) {
                var resource = $resource(config.domain + '/mobile/forget/vcode'),
                    deferred = $q.defer();

                resource.save({
                        mobile: mobile
                    },
                    function (result) {

                        if (result.flag === 1) {
                            deferred.resolve({
                                message: result.msg
                            });
                        } else {
                            deferred.reject({
                                message: result.msg
                            });
                        }
                    },
                    function (data) {
                        console.log(data);
                        deferred.reject({
                            message: '网络异常'
                        });
                    });

                return deferred.promise;
            },
            loginWithQQ: function () {
                var token = 'B9559C8E214B5DA4EA4FFCF31701D380';
                var openID = null;
                var deferred = $q.defer();
                var validateFromBackend = function (args) {
                    var deferred = $q.defer();
                    $http
                        .post(config.domain + '/mobile/oauth/login', {
                            token: token,
                            openid: openID
                        })
                        .success(function (result) {
                            if (result) {
                                if (result.flag == 1) {
                                    deferred.resolve(result.msg);
                                } else {
                                    deferred.reject(result.msg);
                                }
                            } else {
                                return deferred.reject('登录异常');
                            }
                        })
                        .error(function (e) {
                            console.log(e);
                            deferred.reject('登录异常');
                        });

                    return deferred.promise;
                };
                var validateFromQQ = function () {
                    var token;
                    var deferred = $q.defer();
                    var success = false;
                    var handler = window.open('https://graph.qq.com/oauth2.0/authorize?response_type=token&client_id=101204964&redirect_uri=http://scaperow.vicp.cc/api&scope=get_user_info,list_album,upload_pic,add_feeds,do_like', '_blank', 'location=no'); //');
                    handler.addEventListener('exit', function () {
                        if (success) {
                            deferred.resolve(args);
                        } else {
                            deferred.reject('没有完成登录');
                        }
                    });
                    handler.addEventListener('loadstart', function (event) {
                        if (event.url.indexOf("http://scaperow.vicp.cc/api") === 0) {
                            var callbackResponse = (event.url).split("#")[1];
                            var responseParameters = (callbackResponse).split("&");
                            var parameterMap = [];
                            for (var i = 0; i < responseParameters.length; i++) {
                                parameterMap[responseParameters[i].split("=")[0]] = responseParameters[i].split("=")[1];
                            }

                            if (parameterMap.access_token !== undefined && parameterMap.access_token !== null) {
                                token = parameterMap.access_token;
                                success = true;
                            }

                            handler.close();
                        }
                    });

                    return deferred.promise;
                };
                var requestOpenID = function () {
                    var deferred = $q.defer();
                    $http
                        .get('https://graph.qq.com/oauth2.0/me?access_token=' + token)
                        .success(function (result) {
                            var matchResult = result.match(/"openid":"(.*?)"/i);
                            if (matchResult) {
                                openID = matchResult[1];
                            }

                            if (openID) {
                                deferred.resolve({
                                    openID: openID,
                                    token: token
                                });
                            }
                        })
                        .error(function (e) {
                            console.log(e);
                            deferred.reject('登录失败');
                        });

                    return deferred.promise;
                };
                //$q.all[validateFromQQ(), requestOpenID(), validateFromBackend()]
                //    .success(function (result) {
                //
                //    })
                //    .error(function (error) {
                //        deferred.reject(error);
                //    });

                requestOpenID()
                    .then(function () {
                        return validateFromBackend();
                    })
                    .then(function (result) {
                        _current = result;
                        valid = true;
                        localStorage.username = result.username;
                        localStorage.password = result.password;
                        localStorage.with = 'QQ';
                        deferred.resolve(result);
                    })
                    .then(null, function (error) {
                        deferred.reject(error);
                    });

                return deferred.promise;
            },
            address: {
                using: function (address) {
                    if (address) {
                        usingAddress = address;
                    } else {
                        return usingAddress;
                    }
                },
                new: true,
                modify: function (object) {

                },
                /*
                 从服务器获取该id对应的地址信息
                 */
                pull: function (id) {
                },
                /*
                 从本地查找地址信息
                 */
                find: function (id) {

                },
                /*
                 从本地和远程中删除该地址信息
                 */
                del: function (id) {

                }
            }
        };
    })

    /*
     收藏服务
     */
    .factory('Favorite', function ($resource, $q) {
        var local = [];
        if (window.localStorage['favorite']) {
            local = angular.fromJson(window.localStorage['favorite']);
        }

        return {
            mine: [],
            scope: null,
            push: function (userId, items) {
                if (!userId) {
                    return;
                }

                var resource = $resource(config.domain + '/mobile/mergefav');
                resource.save({
                        userid: userId,
                        items: items
                    },
                    function () {

                    },
                    function (err) {
                        console.log(err);
                    });
            },
            merge: function (userId, remote) {
                var deferred = $q.defer();

                local = _.union(local, remote);
                this.push(userId, local);
                this.update(local);
                deferred.resolve();

                return deferred.promise;
            },
            all: function () {
                return local;
            },
            add: function (userId, psid) {
                if (!_.contains(local, psid)) {
                    local.push(psid);
                    this.update(local);
                    this.push(userId, local);
                }
            },
            remove: function (userId, psid) {
                if (_.contains(local, psid)) {
                    local = _.reject(local, function (i) {
                        return i === psid;
                    });

                    this.update(local);
                    this.push(userId, local);
                }

                this.mine = _.reject(this.mine, function (m) {
                    //收藏列表中 id 就是 psid
                    return m.id == psid;
                });
                if (this.scope) {
                    this.scope.items = this.mine;
                }
            },
            update: function (items) {
                window.localStorage.favorite = angular.toJson(items);
                return true;
            },
            contains: function (id) {
                return _.contains(local, id);
            },
            setFavorites: function (favorites) {
                var defered = $q.defer();
                local = favorites;
                defered.resolve();
                return defered.promise;
            }
        }
    })

    /*
     购物车服务
     */
    .factory('ShopCar', function ($resource, $filter, $q, $rootScope) {
        var items = [],
            copies = [],
            payCopies = [],
            gifts = [],
            presaleForDetail = null,
            presales = [],
            useGifts = [],
            payItems = [];

        if (window.localStorage['carItems']) {
            items = angular.fromJson(window.localStorage['carItems']);
        }

        return {
            all: function () {
                return items;
            },
            getGifts: function () {
                return gifts;
            },
            items: items,
            update: function (items) {
                //var saveItems = _.reject(items, function (item) {
                //    return item.isSeckill;
                //});
                //window.localStorage['carItems'] = angular.toJson(saveItems);
                window.localStorage.carItems = angular.toJson(items);
                return true;
            },
            find: function (object) {
                var exists = _.where(items, object);
                if (exists.length > 0) {
                    return exists[0];
                }

                return null;
            },
            fetch: function () {
                var deferred = $q.defer(),
                    resource = $resource(config.domain + '/mobile/shopcar');

                var onlineProducts = [];
                var offlineProducts = [];
                _.map(items, function (item) {
                    if (item.poid && item.poid > 0) {
                        offlineProducts.push(item);
                    } else {
                        onlineProducts.push(item);
                    }
                });

                resource.query({
                    psid: '[' + _.pluck(onlineProducts, 'psid') + ']',
                    poid: '[' + _.pluck(offlineProducts, 'poid') + ']'
                }, function (products) {
                    _.each(products, function (product) {
                        var exists = _.where(items, {
                            psid: product.psid,
                            poid: product.poid
                        });

                        if (exists.length > 0) {
                            exists[0].product = product;
                            exists[0].checked = product.status === 1;
                        }
                    });

                    deferred.resolve(items);
                }, function (error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },
            upload: function (userID, items) {
                var deferred = $q.defer(),
                    resource = $resource(config.domain + '/mobile/mergecar');

                resource.save({
                    userid: userID,
                    items: items
                }, function () {
                    deferred.resolve(items);
                }, function (error) {
                    deferred.reject(error);
                });


                return deferred.promise;
            },
            resume: function (cars) {
                var total = 0;

                _.each(_.where(cars, {
                    checked: true
                }), function (record) {
                    var t = $filter('number')((record.quantity * record.product.price), 2);
                    total += parseFloat(t);
                });

                //if (seckill) {
                //    if (seckill.checked) {
                //        total += parseFloat(seckill.product.msprice);
                //    }
                //}

                total = $filter('number')(total, 2);

                return total;
            },
            remove: function (userId, objects) {

                var newItems = [];

                _.each(items, function (item) {
                    if ((!_.isMatch(item, objects)) || (item.poid && item.poid > 0)) {
                        newItems.push(item);
                    }
                });
                items = newItems;
                this.update(items);

                if (userId) {
                    var resource = $resource(config.domain + '/mobile/mergecar');
                    resource.save({
                        userid: userId,
                        items: items
                    }, function () {

                    }, function (err) {
                        console.log(err);
                    });
                }

                $rootScope.$broadcast('removeCar', {});
            },
            removeOffline: function (userId, objects) {

                var newItems = [];

                _.each(items, function (item) {

                    if ((!_.isMatch(item, objects) ) || (!item.poid || item.poid === 0)) {
                        newItems.push(item);
                    }
                });
                items = newItems;
                this.update(items);

                if (userId) {
                    var resource = $resource(config.domain + '/mobile/mergecar');
                    resource.save({
                        userid: userId,
                        items: items
                    }, function () {

                    }, function (err) {
                        console.log(err);
                    });
                }

                $rootScope.$broadcast('removeCar', {});
            },
            put: function (record) {
                if (record.poid && record.poid > 0) {
                    var exists = this.find({
                        psid: record.psid,
                        poid: record.poid
                    });

                    if (!exists) {
                        items.push(record);
                    }
                } else {
                    var exists = _.where(items, {
                        psid: record.psid
                    });

                    var finded = null;

                    _.each(exists, function (exist) {
                        if (!exist.poid || !exists.poid === 0) {
                            finded = exist;
                        }
                    });

                    if (finded) {
                        finded = record.quantity;
                    } else {
                        items.push(record);
                    }
                }

                this.update(items);
                $rootScope.$broadcast('putCar', {});
            },
            updateFromServer: function (userID) {
                var car = this;
                var resource = $resource(config.domain + '/mobile/profile');

                resource.get({
                        userid: userID
                    },
                    function (data) {
                        if (data.flag === 1) {
                            items = data.cars;
                            car.gifts = data.gifts;
                            car
                                .fetch()
                                .then(function () {
                                    car.update(data.cars);
                                    $rootScope.$broadcast('car:updatedFromServer');
                                });
                        }
                    },
                    function (data) {
                        console.log(data);
                    });
            },
            merge: function (userId, optionals, gifts) {
                //赠品信息保存在内存中，始终从服务器获取
                var deferred = $q.defer();

                this.gifts = gifts;
                _.each(gifts, function (gift) {
                    gift.checked = true;
                });
                _.each(optionals, function (optional) {
                    var exists = _.where(items, {
                        pid: optional.pid,
                        psid: optional.psid
                    });
                    if (exists.length === 0) {
                        items.push(optional);
                    }
                });

                var save = function () {
                    var deferred = $q.defer();
                    window.localStorage['carItems'] = angular.toJson(items);
                    deferred.resolve(items);
                    return deferred.promise;
                };

                this.upload(userId, items)
                    .then(this.fetch)
                    .then(save)
                    .then(function () {
                        $rootScope.$broadcast('car:updatedFromServer');
                        deferred.resolve();
                    })
                    .catch(function (error) {
                        deferred.reject(error);
                        console.log(error);
                    });

                return deferred.promise;
            },
            getCopies: function () {
                return this.copies;
            },
            setCopies: function (copies) {
                this.copies = copies;
            },
            getPayCopies: function () {
                return this.payCopies;
            },
            setPayCopies: function (copies) {
                this.payCopies = copies;
            },
            setPayOptionals: function (optionals) {
                this.payItem = optionals;
            },
            getPayOptionals: function () {
                return this.payItem;
            },
            getUseGifts: function () {
                return this.useGifts;
            },
            setUseGifts: function (gifts) {
                this.useGifts = gifts;
            },
            setGifts: function (gs) {
                var deferred = $q.defer();
                gifts = _.map(gs, function (g) {
                    g.expirs = g.expirs * 1000;
                    g.checked = true;
                    return g;
                });

                deferred.resolve();
                return deferred.promise;
            },
            setOptionals: function (optionals) {
                var car = this,
                    deferred = $q.defer();

                items = optionals;

                this
                    .fetch()
                    .then(function (fetchResult) {
                        items = fetchResult;
                        car.update(items);
                        deferred.resolve();
                    })
                    .catch(function (error) {
                        deferred.reject(error);
                    });

                return deferred.promise;
            },
            setOptionalsWithoutSync: function (optionals) {
                items = optionals;
                this.update(items);
            },
            getPresales: function () {
                return presales;
            },
            putPresales: function (item) {
                //presales.push(item);
                _.where(presales, function (presale) {
                    if(presale.psid === item.id){
                        presale.quantity = item.quantity;
                    } else {
                        presales.push(item);
                    }
                });
            },
            setPresaleForDetail: function (item) {
                presaleForDetail = item;
            },
            getPresaleForDetail: function () {
                return presaleForDetail;
            }
        }
    })

    /*
     *alipay支付服务
     */
    .factory('AliPay', function (Loading, $timeout, $rootScope, $ionicHistory, $q) {
        return {
            pay: function (url, args) {
                var deferred = $q.defer(),
                    args = args,
                    handler = window.open(url, '_blank', 'location=yes,hidden=yes');

                handler.addEventListener('loadstop', function () {
                    Loading.close();
                    handler.show();
                });
                handler.addEventListener('loadstart', function (event) {
                    if (event.url.match('/mobile/alipay_callback')) {
                        handler.close();
                    } else if (event.url.match('/mobile/alipay_cz_callback')) {
                        handler.close();
                    }
                });
                handler.addEventListener('exit', function () {
                    deferred.resolve(args);
                });
                handler.addEventListener('loaderror', function () {
                    deferred.reject();
                });

                return deferred.promise;
            }
            //cz: function (url, $scope, $state) {
            //    $rootScope.hasPaied = false;
            //    var handler = window.open(url, '_blank', 'location=yes,hidden=yes');
            //    handler.addEventListener('loadstop', function () {
            //        Loading.close();
            //        handler.show();
            //    });
            //    handler.addEventListener('loadstart', function (event) {
            //        if (event.url.match('/mobile/alipay_cz_callback')) {
            //            $rootScope.hasPaied = true;
            //            handler.close();
            //        }
            //    });
            //    handler.addEventListener('exit', function () {
            //        if ($rootScope.hasPaied) {
            //            Loading.tip('已完成充值');
            //        } else {
            //            Loading.tip('没有完成充值');
            //        }
            //
            //        //$state.go('tab.account');
            //        $ionicHistory.goBack();
            //    });
            //    handler.addEventListener('loaderror', function () {
            //        Loading.tip('本次支付失败');
            //        //$state.go('tab.account');
            //        $ionicHistory.goBack();
            //    });
            //}
        }
    })

    /*
     *MyOrders支付服务
     */
    .factory('MyOrders', function ($resource) {
        var orders = [];

        var query = function (userId, index, size, type) {
            var params = {
                    index: index || 1,
                    size: size || 5,
                    userid: userId,
                    type: type || 'all'
                },
                resource = $resource(config.domain + '/mobile/order', {}, {
                    query: {
                        isArray: false
                    }
                });

            return resource.query(params);
        };

        return {
            query: query,
            cancelOrder: function (id) {
                var exists = _.where(orders, {
                    id: parseInt(id)
                });
                if (exists.length > 0) {
                    exists[0].status = '已取消';
                    exists[0].scolor = '';
                    exists[0].itemcolor = 'item-stable';
                }
            },
            allOrders: function (userId, index, size) {
                return query(userId, index, size, 'all');
            },
            unPayOrders: function () {
                return query(userId, index, size, 'unpay');
            },
            unWayOrders: function () {
                return query(userId, index, size, 'unway');
            },
            setOrders: function (items) {
                orders = items;
            },
            getOrders: function () {
                return orders;
            }
        }
    })

    /*
     *MyAddress地址服务
     */
    .factory('MyAddress', function (User) {
        var streets = [{
            'K': '碑林区',
            'V': ['南院门街道', '柏树林街道', '长乐坊街道', '东关南街街道', '太乙路街道', '文艺路街道', '长安路街道', '张家村街道']
        },
            {
                'K': '灞桥区',
                'V': ['纺织城街道', '十里铺街道', '红旗街道', '席王街道', '洪庆街道', '狄寨街道', '灞桥街道', '新筑街道', '新合街道']
            },
            {
                'K': '长安区',
                'V': ['韦曲街道', '郭杜街道', '引镇街道', '王寺街道', '滦镇街道', '马王街道', '太乙宫街道', '东大街道', '子午街道', '斗门街道', '细柳街道', '杜曲街道', '大兆街道', '兴隆街道', '黄良街道']
            },
            {
                'K': '莲湖区',
                'V': ['青年路街道', '北院门街道', '北关街道', '红庙坡街道', '环城西路街道', '西关街道', '土门街道', '桃园路街道', '枣园街道']
            },
            {
                'K': '未央区',
                'V': ['张家堡街道', '三桥街道', '辛家庙街道', '徐家湾街道', '大明宫街道', '谭家街道', '草滩街道', '未央宫街道', '汉城街道', '六村堡街道']
            },
            {
                'K': '新城区',
                'V': ['西一路街道', '长乐中路街道', '中山门街道', '韩森寨街道', '解放门街道', '自强路街道', '太华路街道', '长乐西路街道', '胡家庙街道']
            },
            {
                'K': '雁塔区',
                'V': ['小寨路街道', '大雁塔街道', '长延堡街道', '电子城街道', '等驾坡街道', '鱼化寨街道', '丈八沟街道', '曲江街道']
            },
            {
                'K': '高新区',
                'V': ['全部地区']
            }];
        return {
            newAddress: function (obj, addresses) {
                addresses.push(obj);
            },
            delAddress: function (id, $scope) {
                var user = User.current();
                if (user) {
                    var exists = _.where(user.addresses, {
                        id: parseInt(id)
                    });
                    if (exists.length > 0) {
                        user.addresses = _.without(user.addresses, exists[0]);
                    }
                }
            },
            getDefaultAddress: function (addresses) {
                var exists = _.where(addresses, {
                    isdefault: 1
                });
                if (exists.length > 0) {
                    return exists[0];
                }
                if (addresses.length > 0) {
                    return addresses[0];
                }
                return null;
            },
            updateAddress: function (obj, addresses) {
                var exists = _.where(addresses, {
                    id: parseInt(obj.id)
                });
                if (exists.length > 0) {
                    exists[0].address = obj.address;
                    exists[0].province = obj.province;
                    exists[0].city = obj.city;
                    exists[0].mobile = obj.mobile;
                    exists[0].tel = obj.tel;
                    exists[0].name = obj.name;
                }
            },
            setDefaultAddress: function (id, addresses) {
                _.each(addresses, function (item) {
                    if (item.id == id) {
                        item.isdefault = 1;
                    } else {
                        item.isdefault = 0;
                    }
                });
            },
            getAddressByID: function (id, addresses) {
                var exists = _.where(addresses, {
                    id: parseInt(id)
                });
                if (exists.length > 0) {
                    return exists[0];
                }
                return null;
            },
            getCurrentStreets: function (region) {
                items = [];
                _.each(streets, function (item) {
                    if (item['K'] == region) {
                        items = item['V'];
                    }
                });
                return items;
            }
        }
    })

    /*
     加载框
     */
    .factory('Loading', function ($ionicLoading) {
        return {
            show: function (delay) {
                delay = delay || 1000;
                $ionicLoading.show({
                    delay: delay
                });
            },
            tip: function (message, duration) {
                duration = duration || 2000;
                $ionicLoading.hide();
                $ionicLoading.show({
                    template: message,
                    duration: duration,
                    noBackdrop: true
                });
            },
            close: function () {
                $ionicLoading.hide();
            }
        }
    })

    .factory('SearchKeywords', function ($resource) {
        var localKeywords = [],
            hots = [];

        try {
            localKeywords = angular.fromJson(localStorage.searchKeywords);
        } catch (e) {
            localKeywords = [];
        }

        if (!localKeywords) {
            localKeywords = [];
        }

        return {
            hots: function (array) {
                if (array) {
                    hots = array;
                } else {
                    return hots;
                }
            },
            local: function () {
                return localKeywords;
            },
            add: function (keyword) {
                var idx = localKeywords.indexOf(keyword);
                if (idx >= 0) {
                    localKeywords.splice(idx, 1);
                }
                localKeywords.splice(0, 0, keyword);
                localStorage.searchKeywords = angular.toJson(localKeywords);
            },
            clearLocalKeyword: function () {
                localKeywords = [];
                localStorage.searchKeywords = angular.toJson(localKeywords);
            }
        }
    })

    /*
     http 拦截器，所有的网络请求都会先经过于此
     */
    .factory('HttpInterceptor', function ($q, $rootScope) {
        var interceptor = {
            'responseError': function (rejection) {
                var deferred = $q.defer();
                if (rejection && rejection.status === 401) {
                    $rootScope.$broadcast('user:requireLogin', {
                        deferred: deferred
                    });
                    return deferred.promise;
                } else {
                    return rejection;
                }
            },
            'request': function (http) {
                switch (http.method) {
                    case 'GET':
                        http.params = _.extend({
                            version: config.version
                        }, http.params);
                        break;

                    case 'POST':
                        http.url += '?version=' + config.version;
                        break;
                }

                return http;
            }

        };

        return interceptor;
    });