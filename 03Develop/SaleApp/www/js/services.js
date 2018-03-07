angular.module('starter.services', ['ngResource'])
  .config(function($httpProvider) {
    $httpProvider.defaults.headers.post = {
      'Authorization': 'Basic ' + btoa(localStorage.username + ':' + localStorage.password),
      'Access-Control-Allow-Origin': config.domain
    };

    $httpProvider.interceptors.push('HttpInterceptor');
  })
  /*
   首页广告的数据服务
   */
  .factory('Ad', function($resource, $http, $rootScope, $q) {
    var ads = [];

    return {
      /*
       从服务器上获取一次数据
       */

      fetch: function(cityId) {
        var deferred = $q.defer();
        $http
          .get(config.domain + '/mobile/ads', {
            cityid: cityId
          })
          .success(function(result) {
            ads = _.map(result, function(item) {
              item.img = config.domain + '/upload/ad/' + item.img;
              item.href = JSON.parse(item.href || null);
              return item;
            });
            deferred.resolve(ads);
          })
          .catch(function() {
            deferred.reject();
          });

        return deferred.promise;
      },
      /*
       返回广告缓存
       */
      cache: function() {
        return ads;
      },
      /*
       根据某一个id获取广告
       */
      get: function(id) {
        var exists = [];
        _.each(ads, function(ad) {
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
  /*
   首页产品的数据服务
   */
  .factory('Products', function($resource, $rootScope, $q, $http, SearchKeywords) {
    var source = {};

    return {
      /*从服务器上获取一次数据*/
      refresh: function() {
        var deferred = $q.defer();
        $http
          .get(config.domain + '/mobile/home')
          .success(function(result) {
            source.products = _.map(result.products, function(item) {
              item.cover = config.domain + item.cover;
              return item;
            });

            source.stores = _.map(result.stores, function(item) {
              item.cover = config.domain + '/' + item.cover;
              return item;
            });

            SearchKeywords.hots(result.k);

            deferred.resolve(source);
          })
          .catch(function() {
            console.log('erererer');
            deferred.reject();
          });

        return deferred.promise;
      },
      /*获取所有商品的缓存数据*/
      cache: function() {
        return source;
      }
    }
  })
  /*
   用户数据服务
   */
  .factory('User', function($resource, $q, $rootScope, $http, $timeout, ShopCar, Favorite) {
    var _current = null,
      valid = false,
      location = null,
      city = null,
      url = config.domain + '/mobile/login',
      resource = $resource(url);
    try {
      city = JSON.parse(localStorage.city || 'null');
    } catch (e) {

    }
    return {
      /*
       充值密码
       */
      resetPassword: function(mobile, password) {
        var resource = $resource(config.domain + '/mobile/resetpassword'),
          deferred = $q.defer();
        resource.save({
            password: password,
            apassword: password,
            mobile: mobile
          },
          function(result) {
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
          function(data) {
            console.log(data);
            deferred.reject({
              message: '网络异常'
            });
          });

        return deferred.promise;
      },
      /*获取当前登录的用户*/
      current: function() {
        return _current;
      },
      hasValid: function() {
        return valid;
      },
      valided: function() {
        valid = true;
      },
      setUser: function(user) {
        _current = user;
      },
      setLocation: function(l) {
        location = l;
      },
      setCity: function(c) {
        city = c;
        localStorage.city = JSON.stringify(c);
        $rootScope.$broadcast('location:setCity', {
          city: c
        });
      },
      getCity: function() {
        return city;
      },
      getLocation: function() {
        return location;
      },
      /*
       从后台登录
       */
      loginBackend: function() {
        var name = localStorage['username'],
          password = localStorage['password'],
          deferred = $q.defer();

        if (name && password) {
          this
            .login(name, password)
            .then(this.updateProfile)
            .then(function() {
              deferred.resolve();
            })
            .catch(function(err) {
              deferred.reject(err);
            });
        } else {
          deferred.reject();
        }

        return deferred.promise;
      },
      /*注销用户*/
      logout: function() {
        localStorage.clear();
        _current = null;
        valid = false;
      },
      /*登录方法*/
      login: function(userName, password) {
        var deferred = $q.defer();
        var position = {
          x: '',
          y: '',
          province: '',
          city: '',
          region: '',
          address: ''
        };

        if (location) {
          position = {
            x: location.x,
            y: location.y,
            province: location.address.province,
            city: location.address.city,
            region: location.address.district,
            address: location.address.street + location.address.streetNumber
          };
        }

        resource.save(_.extend({
            mobile: userName,
            password: password,
            login_type: 1
          }, position),
          function(result) {
            if (result.flag === 1) {
              _current = result['msg'];
              valid = true;


              if(_current.store) {
                if (_current.store.image && _current.store.image.length > 0) {
                  _current.store.image = config.domain + _current.store.image;
                } else {
                  _current.store.image = 'img/banner.png';
                }
              }
              if(_current.store) {
                if (_current.store.image_license && _current.store.image_license.length > 0) {
                  _current.store.image_license = config.domain + _current.store.image_license.image;
                } else {
                  _current.store.image_license = 'img/nopic.png';
                }
              }
              if(_current.store) {
                if (_current.store.image_legal && _current.store.image_legal.length > 0) {
                  _current.store.image_legal = config.domain + _current.store.image_legal;
                } else {
                  _current.store.image_legal = 'img/nopic.png';
                }
              }
              localStorage.username = userName;
              localStorage.password = password;
              localStorage.store = JSON.stringify( _current.store);
              localStorage.with = '';
              deferred.resolve(result);
              $rootScope.$broadcast('loginSuccess', result);
            } else {
              _current = null;
              valid = false;
              deferred.reject(result);
              $rootScope.$broadcast('loginFail', result);
            }
          //},
          //function(err) {
          //  _current = null;
          //  valid = false;
          //  deferred.reject(err);
          //  $rootScope.$broadcast('loginFail', err);
          //});
          },
          function(err) {
            _current = null;
            valid = false;
            deferred.reject(err);
            $rootScope.$broadcast('loginFail', err);
          });

        return deferred.promise;
      },
      /*从服务器上获取当前用户的个人数据 */
      updateProfile: function() {
        var deferred = $q.defer(),
          resource = $resource(config.domain + '/mobile/profile');

        if (_current) {
          resource.get({
              userid: _current.id
            },
            function(data) {
              if (data.flag == 1) {
                var shopCar = data.cars;
                var gifts = data.gifts;

                $q.all([ShopCar.setOptionals(shopCar), Favorite.setFavorites(data.favorites, data.fav_stores)])
                  .then(function() {
                    $rootScope.$broadcast('user:updateProfileSuccess');
                    deferred.resolve();
                  })
                  .catch(function(error) {
                    console.log(error);
                    deferred.resolve(error);
                    $rootScope.$broadcast('user:updateProfileFail');
                  });

              } else {
                deferred.resolve();
              }
            },
            function(data) {
              console.log(data);
            });
        } else {
          // $rootScope.$broadcast('user:updateProfileSuccess');
          deferred.resolve();
        }

        return deferred.promise;
      },
      /*同步用户的个人数据 */
      syncProfile: function() {
        var deferred = $q.defer(),
          resource = $resource(config.domain + '/mobile/profile');

        if (valid) {
          resource.get({
              userid: _current.id
            },
            function(data) {
              if (data.flag == 1) {
                var optionals = data.cars;
                $q.all([ShopCar.merge(_current.id, optionals), Favorite.merge(_current.id, data.favorites, data.fav_stores)])
                  .then(function() {
                    deferred.resolve();
                  })
                  .catch(function(err) {
                    console.log(err);
                    deferred.reject(err);
                  });
              }
            },
            function(data) {
              console.log(data);
            });
        } else {
          deferred.reject('用户未登录');
        }

        return deferred.promise;
      },
      /* 向服务器请求发送用户修改密码的验证码*/
      requestValidationCodeModify: function(mobile) {
        var resource = $resource(config.domain + '/mobile/changepassword/vcode'),
          deferred = $q.defer();

        resource.get({
            mobile: mobile
          },
          function(result) {

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
          function(data) {
            console.log(data);
            deferred.reject({
              message: '网络或服务器异常'
            });
          });

        return deferred.promise;
      },
      /* 向服务器请求发送用于注册的验证码*/
      requestValidationCodeRegister: function(mobile) {
        var resource = $resource(config.domain + '/mobile/vcode'),
          deferred = $q.defer();

        resource.get({
            mobile: mobile
          },
          function(result) {

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
          function(data) {
            console.log(data);
            deferred.reject({
              message: '网络异常'
            });
          });

        return deferred.promise;
      },
      /*修改用户密码*/
      requestResetPassword: function(validationCode, mobile) {
        var resoruce = $resource(config.domain + '/mobile/forgotpassword'),
          deferred = $q.defer();

        //resoruce.save({
        //    mobile: mobile,
        //    vcode: validationCode
        //  },
        //  function(result) {
        //    if (result.flag === 1) {
        deferred.resolve();
        //  } else {
        //    deferred.reject({
        //      message: result.msg
        //    });
        //  }
        //},
        //function(error) {
        //  deferred.reject({
        //    message: '网络异常'
        //  });
        //});

        return deferred.promise;
      },
      /* 向服务器请求发送用于忘记密码的验证码*/
      requestValidationCodeRecovery: function(mobile) {
        var resource = $resource(config.domain + '/mobile/forget/vcode'),
          deferred = $q.defer();

        resource.save({
            mobile: mobile
          },
          function(result) {

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
          function(data) {
            console.log(data);
            deferred.reject({
              message: '网络异常'
            });
          });

        return deferred.promise;
      },
      loginWithQQ: function() {
        var token = 'B9559C8E214B5DA4EA4FFCF31701D380';
        var openID = null;
        var deferred = $q.defer();
        var validateFromBackend = function(args) {
          var deferred = $q.defer();
          $http
            .post(config.domain + '/mobile/oauth/login', {
              token: token,
              openid: openID
            })
            .success(function(result) {
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
            .error(function(e) {
              console.log(e);
              deferred.reject('登录异常');
            });

          return deferred.promise;
        };
        var validateFromQQ = function() {
          var token;
          var deferred = $q.defer();
          var success = false;
          var handler = window.open('https://graph.qq.com/oauth2.0/authorize?response_type=token&client_id=101204964&redirect_uri=http://scaperow.vicp.cc/api&scope=get_user_info,list_album,upload_pic,add_feeds,do_like', '_blank', 'location=no'); //');
          handler.addEventListener('exit', function() {
            if (success) {
              deferred.resolve(args);
            } else {
              deferred.reject('没有完成登录');
            }
          });
          handler.addEventListener('loadstart', function(event) {
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
        var requestOpenID = function() {
          var deferred = $q.defer();
          $http
            .get('https://graph.qq.com/oauth2.0/me?access_token=' + token)
            .success(function(result) {
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
            .error(function(e) {
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
          .then(function() {
            return validateFromBackend();
          })
          .then(function(result) {
            _current = result;
            valid = true;
            localStorage.username = result.username;
            localStorage.password = result.password;
            localStorage.with = 'QQ';
            deferred.resolve(result);
          })
          .then(null, function(error) {
            deferred.reject(error);
          });

        return deferred.promise;
      },
      address: {
        /*获取或设置路由器中临时使用的地址*/
        using: function(address) {
          if (address) {
            usingAddress = address;
          } else {
            return usingAddress;
          }
        },
        modify: function(object) {

        },
        /*
         从服务器获取该id对应的地址信息
         */
        pull: function(id) {},
        /*
         从本地查找地址信息
         */
        find: function(id) {

        },
        /*
         从本地和远程中删除该地址信息
         */
        del: function(id) {

        }
      }
    };
  })
  /*
   收藏商品的数据服务
   */
  .factory('Favorite', function($resource, $http, $q) {
    var products = JSON.parse(window.localStorage.FavoriteProducts || '[]') || [];
    var stores = JSON.parse(window.localStorage.FavoriteStores || '[]') || [];

    return {
      /*在本地合并收藏商品并覆盖到服务器*/
      merge: function(userID, remoteProducts, remoteStores) {
        products = _.union(products, remoteProducts);
        stores = _.union(stores, remoteStores);
        window.localStorage.FavoriteProducts = JSON.stringify(products);
        window.localStorage.FavoriteStores = JSON.stringify(stores);
        // this.update(products);
        this.saveToServer(userID);
      },
      saveToServer: function(userID) {
        if (userID) {
          $http.post(config.domain + '/mobile/mergefav', {
            items: products,
            stores: stores,
            userid: userID
          });
        }
      },
      /*获取所有的收藏商品缓存数据*/
      getProducts: function() {
        return products;
      },
      getStores: function() {
        return stores;
      },
      /*添加一个收藏商品并覆盖到服务器*/
      favoriteProduct: function(userID, psid) {
        if (!_.contains(products, psid)) {
          products.push(psid);
          localStorage.FavoriteProducts = JSON.stringify(products);
          this.saveToServer(userID);
        }
      },
      favoriteStore: function(userID, storeID) {
        if (!_.contains(stores, storeID)) {
          stores.push(storeID);
          localStorage.FavoriteStores = JSON.stringify(stores);
          this.saveToServer(userID);
        }
      },
      /*移除一个收藏商品*/
      removeProduct: function(userID, psid) {
        if (_.contains(products, psid)) {
          products = _.reject(products, function(i) {
            return i === psid;
          });

          localStorage.FavoriteProducts = JSON.stringify(products);
          this.saveToServer(userID);
        }
      },
      containsProduct: function(psid) {
        return _.contains(products, psid);
      },
      containsStore: function(storeID) {
        return _.contains(stores, storeID);
      },
      removeStore: function(userID, storeID) {
        if (_.contains(stores, storeID)) {
          stores = _.reject(stores, function(i) {
            return i === storeID;
          });

          localStorage.FavoriteStores = JSON.stringify(stores);
          this.saveToServer(userID);
        }
      },
      /*更新本地缓存*/
      setFavorites: function(products, stores) {
        products = products;
        stores = stores;
        window.localStorage.FavoriteProducts = JSON.stringify(products);
        window.localStorage.FavoriteStores = JSON.stringify(stores);
      }
    }
  })
  /*
   购物车服务
   */
  .factory('ShopCar', function($resource, $filter, $http, $q, $rootScope) {
    var items = [],
      payItems = [];

    if (window.localStorage['carItems']) {
      items = angular.fromJson(window.localStorage['carItems']);
    }

    return {
      /*返回所有的购物车信息*/
      all: function() {
        return items;
      },
      /*根据键值对查找出对应的购物车数据*/
      find: function(object) {
        var exists = _.where(items, object);
        if (exists.length > 0) {
          return exists[0];
        }

        return null;
      },
      fetchProduct: function() {
        var deferred = $q.defer();

        $http
          .get(config.domain + '/mobile/shopcar', {
            params: {
              psid: JSON.stringify(_.map(items, function(item) {
                return item.psid
              }))
            }
          })
          .success(function(result) {
            _.each(result, function(product) {
              product.cover = config.domain + product.cover;
              var exists = _.find(items, function(item) {
                return item.psid === product.psid;
              });

              if (exists) {
                exists.product = product;
                exists.checked = product.status === 1;
              }
            });

            window.localStorage.carItems = angular.toJson(items);

            deferred.resolve(items);
          })
          .catch(function(error) {
            console.log(error);
            deferred.reject(error);
          });

        return deferred.promise;
      },
      /*覆盖服务器的购物车数据*/
      upload: function(userID) {
        var deferred = $q.defer(),
          resource = $resource();

        $http
          .post(config.domain + '/mobile/mergecar', {
            userid: userID,
            items: items
          }).success(function() {
            deferred.resolve(items);
          })
          .catch(function(error) {
            deferred.reject(error);
          });

        return deferred.promise;
      },
      /*统计购物车合计*/
      resumeTotalPrice: function(cars) {
        var total = 0;

        _.each(_.where(cars, {
          checked: true
        }), function(record) {
          var t = $filter('number')((record.quantity * record.product.price), 2);
          total += parseFloat(t);
        });

        total = $filter('number')(total, 2);

        return total;
      },
      /*从购物车中移除某一项商品并同步到服务器*/
      remove: function(userId, id) {
        var deferred = $q.defer();

        items = _.reject(items, function(item) {
          return item.psid === id;
        });

        window.localStorage.carItems = angular.toJson(items);

        if (userId) {
          $http
            .post(config.domain + '/mobile/mergecar', {
              userid: userId,
              items: items
            })
            .success(function(result) {
              deferred.resolve();
              $rootScope.$broadcast('shopCar:removeItemSuccess');
            })
            .catch(function(error) {
              console.log(error);
              deferred.reject();
            });
        } else {
          deferred.resolve();
          $rootScope.$broadcast('shopCar:removeItemSuccess');
        }

        return deferred.promise;
      },
      /*将某一件商品放入购物车*/
      put: function(record) {
        var exists = _.find(items, function(item) {
          return item.psid === record.psid;
        });

        if (exists) {
          exists = record.quantity;
        } else {
          items.push(_.extend(_.pick(record, 'psid', 'pid'), {
            quantity: 1
          }));
        }

        $rootScope.$broadcast('shopCar:addItemSuccess', {});
      },
      /*合并购物车、赠品数据*/
      merge: function(userID, optionals) {
        //赠品信息保存在内存中，始终从服务器获取
        var deferred = $q.defer();

        items = optionals;
        this.upload(userID, items)
          .then(function() {
            window.localStorage.carItems = angular.toJson(items);
          })
          .then(function() {
            // $rootScope.$broadcast('car:updatedFromServer');
            deferred.resolve();
          })
          .catch(function(error) {
            deferred.reject(error);
            console.log(error);
          });

        return deferred.promise;
      },
      clear: function(userID) {
        var deferred = $q.defer();

        items = [];

        window.localStorage.carItems = angular.toJson(items);

        if (userID) {
          $http
            .post(config.domain + '/mobile/mergecar', {
              userid: userID,
              items: items
            })
            .success(function(result) {
              deferred.resolve();
              $rootScope.$broadcast('shopCar:removeItemSuccess');
            })
            .catch(function(error) {
              console.log(error);
              deferred.reject();
            });
        } else {
          deferred.resolve();
          $rootScope.$broadcast('shopCar:removeItemSuccess');
        }

        return deferred.promise;
      },
      setPayOptionals: function(optionals) {
        this.payItem = optionals;
      },
      /*获取自选商品的待支付的临时数据*/
      getPayOptionals: function() {
        return this.payItem;
      },
      /*设置自选商品并与服务器同步*/
      setOptionals: function(optionals) {
        items = optionals;
        window.localStorage.carItems = angular.toJson(items);
      },
      /*设置自选商品不同步*/
      setOptionalsWithoutSync: function(optionals) {
        items = optionals;
        this.update(items);
      }
    }
  })
  /*
   *alipay支付服务
   */
  .factory('AliPay', function(Loading, $timeout, $rootScope, $ionicHistory, $q) {
    return {
      pay: function(url, args) {
        var deferred = $q.defer(),
          args = args,
          handler = window.open(url, '_blank', 'location=yes,hidden=yes');

        handler.addEventListener('loadstop', function() {
          Loading.close();
          handler.show();
        });
        handler.addEventListener('loadstart', function(event) {
          if (event.url.match('/mobile/alipay_callback')) {
            handler.close();
          } else if (event.url.match('/mobile/alipay_cz_callback')) {
            handler.close();
          }
        });
        handler.addEventListener('exit', function() {
          deferred.resolve(args);
        });
        handler.addEventListener('loaderror', function() {
          deferred.reject();
        });

        return deferred.promise;
      }
    }
  })
  .factory('Store', function(Loading, $http, $timeout, $rootScope, $ionicHistory, $q, User) {
    var stores = [],
      selected = null;

    return {
      getStoresNearby: function(location) {
        var deferred = $q.defer();
        var stores = [{
          id: 1,
          name: '车之翼汽车维护专家',
          distance: 1,
          stars: 5,
          img: 'http://e.hiphotos.baidu.com/bainuo/crop%3D0%2C21%2C690%2C418%3Bw%3D470%3Bq%3D80/sign=9cb23fc830d3d539d572558307b7c562/2e2eb9389b504fc2803aaf33e3dde71190ef6d9a.jpg',
          description: '史上最强的车辆维护'
        }, {
          id: 2,
          name: '爱车之家汽车保养维修',
          distance: 1.5,
          stars: 4,
          img: 'http://e.hiphotos.baidu.com/bainuo/crop%3D0%2C21%2C690%2C418%3Bw%3D470%3Bq%3D80/sign=0744dc967b1ed21b6d8674a5905ef1f6/b219ebc4b74543a902f6b7a818178a82b80114e0.jpg',
          description: '史上最强的车辆维护'
        }, {
          id: 3,
          name: '汽车大全',
          distance: 3,
          stars: 3,
          img: 'http://e.hiphotos.baidu.com/bainuo/crop%3D0%2C1%2C718%2C435%3Bw%3D470%3Bq%3D99/sign=a9679055a2efce1bfe64928a9261dfef/0b7b02087bf40ad15b511440522c11dfa8ecced8.jpg',
          description: '史上最强的车辆维护'
        }, {
          id: 4,
          name: '恒鼎汽车大全',
          distance: 8,
          stars: 3,
          img: 'http://e.hiphotos.baidu.com/bainuo/crop%3D0%2C48%2C690%2C418%3Bw%3D470%3Bq%3D79/sign=5349d6e8b14543a9e154a08c2327a6b6/1c950a7b02087bf4ea815ff5f4d3572c11dfcfb9.jpg',
          description: '史上最强的车辆维护'
        }];
        deferred.resolve(stores);
        /*
         var user = User.current();
         $http
         .get(config.domain + '/stores', {params: {uid: user.id}})
         .success(function (result) {

         })
         .error(function () {

         });
         */

        return deferred.promise;
      }
    }
  })
  /*
   *MyOrders支付服务
   */
  .factory('MyOrders', function($resource) {
    var orders = [];

    var query = function(userId, index, size, type) {
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
      /*取消某一个订单*/
      cancelOrder: function(id) {
        var exists = _.where(orders, {
          id: parseInt(id)
        });
        if (exists.length > 0) {
          exists[0].status = '已取消';
          exists[0].scolor = '';
          exists[0].itemcolor = 'item-stable';
        }
      },
      /*从服务器获取订单数据*/
      allOrders: function(userId, index, size) {
        return query(userId, index, size, 'all');
      },
      /*获取没有支付的订单*/
      unPayOrders: function() {
        return query(userId, index, size, 'unpay');
      },
      /*获取运送在途的订单*/
      unWayOrders: function() {
        return query(userId, index, size, 'unway');
      },
      /*设置订单数据*/
      setOrders: function(items) {
        orders = items;
      },
      /*设置订单缓存数据*/
      getOrders: function() {
        return orders;
      }
    }
  })
  /*
   *StoreOrders属于门店的订单
   */
  .factory('StoreOrders', function($resource) {
    var orders = [];

    var query = function(store_id, index, size, type) {
      var params = {
          index: index || 1,
          size: size || 5,
          store_id: store_id,
          type: type || 'all'
        },
        resource = $resource(config.domain + '/mobile/store_order', {}, {
          query: {
            isArray: false
          }
        });

      return resource.query(params);
    };

    return {
      query: query,
      /*取消某一个订单*/
      cancelOrder: function(id) {
        var exists = _.where(orders, {
          id: parseInt(id)
        });
        if (exists.length > 0) {
          exists[0].status = '已取消';
          exists[0].scolor = '';
          exists[0].itemcolor = 'item-stable';
        }
      },
      /*从服务器获取订单数据*/
      allOrders: function(userId, index, size) {
        return query(userId, index, size, 'all');
      },
      /*获取没有支付的订单*/
      unPayOrders: function() {
        return query(userId, index, size, 'unpay');
      },
      /*获取运送在途的订单*/
      unWayOrders: function() {
        return query(userId, index, size, 'unway');
      },
      /*设置订单数据*/
      setOrders: function(items) {
        orders = items;
      },
      /*设置订单缓存数据*/
      getOrders: function() {
        return orders;
      }
    }
  })
  /*
   *MyAddress地址服务
   */
  .factory('MyAddress', function(User, $http) {
    /********** 省份数据 **********/
    var GP = new Array("北京", '陕西');
    /********** 市级数据 **********/
    var GC1 = new Array();
    GC1['陕西'] = new Array('西安', '安康', '宝鸡', '汉中', '商洛', '铜川', '渭南', '咸阳', '延安', '榆林');
    GC1['北京'] = new Array('昌平', '朝阳', '崇文', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟', '密云', '平谷', '石景山', '顺义', '通州', '西城', '宣武', '延庆');
    /********** 县乡数据 **********/
    var GC2 = new Array();
    GC2['陕西'] = new Array();
    GC2['陕西']['西安'] = new Array('碑林区', '莲湖区', '新城区', '雁塔区', '未央区', '灞桥区', '长安区'); //'高陵','户县','蓝田','西安市','周至','临潼区','阎良区',
    GC2['陕西']['安康'] = new Array('安康市', '白河', '汉阴', '岚皋', '宁陕', '平利', '石泉', '旬阳', '镇坪', '紫阳', '汉滨区');
    GC2['陕西']['宝鸡'] = new Array('宝鸡市', '凤县', '凤翔', '扶风', '麟游', '陇县', '眉县', '岐山', '千阳', '太白', '陈仓区', '金台区', '渭滨区');
    GC2['陕西']['汉中'] = new Array('城固', '佛坪', '汉中市', '留坝', '略阳', '勉县', '南郑', '宁强', '西乡', '洋县', '镇巴', '汉台区');
    GC2['陕西']['商洛'] = new Array('丹凤', '洛南', '山阳', '商洛市', '商南', '镇安', '柞水', '商州区');
    GC2['陕西']['铜川'] = new Array('铜川市', '宜君', '王益区', '耀州区', '印台区');
    GC2['陕西']['渭南'] = new Array('白水', '澄城', '大荔', '富平', '韩城', '合阳', '华县', '华阴', '蒲城', '潼关', '渭南市', '临渭区');
    GC2['陕西']['咸阳'] = new Array('彬县', '长武', '淳化', '泾阳', '礼泉', '乾县', '三原', '武功', '咸阳市', '兴平', '旬邑', '永寿', '秦都区', '渭城区', '杨陵区');
    GC2['陕西']['延安'] = new Array('安塞', '富县', '甘泉', '黄陵', '黄龙', '洛川', '吴起', '延安市', '延长', '延川', '宜川', '志丹', '子长', '宝塔区');
    GC2['陕西']['榆林'] = new Array('定边', '府谷', '横山', '佳县', '靖边', '米脂', '清涧', '神木', '绥德', '吴堡', '榆林市', '子洲', '榆阳区');

    GC2['北京'] = new Array();
    GC2['北京']['昌平'] = new Array('昌平');
    GC2['北京']['朝阳'] = new Array('朝阳');
    GC2['北京']['崇文'] = new Array('崇文');
    GC2['北京']['大兴'] = new Array('大兴');
    GC2['北京']['东城'] = new Array('东城');
    GC2['北京']['房山'] = new Array('房山');
    GC2['北京']['丰台'] = new Array('丰台');
    GC2['北京']['海淀'] = new Array('海淀');
    GC2['北京']['怀柔'] = new Array('怀柔');
    GC2['北京']['门头沟'] = new Array('门头沟');
    GC2['北京']['密云'] = new Array('密云');
    GC2['北京']['平谷'] = new Array('平谷');
    GC2['北京']['石景山'] = new Array('石景山');
    GC2['北京']['顺义'] = new Array('顺义');
    GC2['北京']['通州'] = new Array('通州');
    GC2['北京']['西城'] = new Array('西城');
    GC2['北京']['宣武'] = new Array('宣武');
    GC2['北京']['延庆'] = new Array('延庆');

    var GC3 = new Array();
    GC3['陕西'] = new Array();
    GC3['陕西']['西安'] = new Array();
    GC3['陕西']['西安']['碑林区'] = new Array('柏树林街道', '长安路街道', '长乐坊街道', '东关南街街道', '南院门街道', '太乙路街道', '文艺路街道', '张家村街道');
    GC3['陕西']['西安']['长安区'] = new Array('大兆街道', '东大街道', '斗门街道', '杜曲街道', '郭杜街道', '黄良街道', '滦镇街道', '马王街道', '太乙宫街道', '王寺街道', '韦曲街道', '细柳街道', '兴隆街道', '引镇街道', '子午街道'); //'高桥乡','王莽乡','王曲镇','鸣犊镇','炮里乡','灵沼乡','魏寨乡','五台乡','五星乡','杨庄乡',
    GC3['陕西']['西安']['莲湖区'] = new Array('北关街道', '北院门街道', '红庙坡街道', '环城西路街道', '青年路街道', '桃园路街道', '土门街道', '西关街道', '枣园街道');
    GC3['陕西']['西安']['未央区'] = new Array('张家堡街道', '三桥街道', '辛家庙街道', '徐家湾街道', '大明宫街道', '谭家街道', '草滩街道', '未央宫街道', '汉城街道', '六村堡街道');
    GC3['陕西']['西安']['临潼区'] = new Array('北田镇', '代王街道', '何寨镇', '交口镇', '零口街道', '马额街道', '穆寨乡', '秦陵街道', '任留乡', '铁炉乡', '土桥乡', '西泉街道', '相桥街道', '小金乡', '斜口街道', '新丰街道', '新市街道', '行者街道', '徐杨街道', '油槐镇', '雨金街道', '骊山街道', '栎阳街道');
    GC3['陕西']['西安']['新城区'] = new Array('长乐西路街道', '长乐中路街道', '韩森寨街道', '胡家庙街道', '解放门街道', '太华路街道', '西一路街道', '中山门街道', '自强路街道');
    GC3['陕西']['西安']['阎良区'] = new Array('北屯街道', '凤凰路街道', '关山镇', '武屯镇', '新华路街道', '新兴街道', '振兴街道');
    GC3['陕西']['西安']['雁塔区'] = new Array('长延堡街道', '大雁塔街道', '等驾坡街道', '电子城街道', '曲江街道', '小寨路街道', '鱼化寨街道', '丈八沟街道');
    GC3['陕西']['西安']['灞桥区'] = new Array('狄寨街道', '纺织城街道', '洪庆街道', '红旗街道', '十里铺街道', '席王街道', '新合街道', '新筑街道', '灞桥街道');
    GC3['陕西']['西安']['高陵'] = new Array('崇皇乡', '耿镇', '鹿苑镇', '通远镇', '湾子乡', '榆楚乡', '张卜乡', '泾渭镇');
    GC3['陕西']['西安']['户县'] = new Array('苍游乡', '草堂镇', '大王镇', '甘河镇', '甘亭镇', '蒋村镇', '涝店镇', '庞光镇', '秦渡镇', '石井镇', '天桥乡', '渭丰乡', '五竹乡', '余下镇', '玉蝉乡', '祖庵镇');
    GC3['陕西']['西安']['蓝田'] = new Array('安村乡', '葛牌镇', '厚镇乡', '华胥镇', '焦岱镇', '金山乡', '九间房乡', '蓝关镇', '蓝桥乡', '孟村乡', '普化镇', '前卫镇', '三官庙乡', '三里镇', '史家寨乡', '汤峪镇', '小寨乡', '泄湖镇', '玉川乡', '玉山镇', '灞源乡', '辋川乡');
    GC3['陕西']['西安']['周至'] = new Array('板房子乡', '陈河乡', '翠峰乡', '二曲镇', '富仁乡', '广济镇', '侯家村乡', '厚畛子镇', '集贤镇', '九峰乡', '楼观镇', '骆峪乡', '马召镇', '青化乡', '尚村镇', '司竹乡', '四屯乡', '王家河乡', '辛家寨乡', '哑柏镇', '终南镇', '竹峪乡');

    GC3['北京'] = new Array();
    GC3['北京']['昌平'] = new Array();
    GC3['北京']['昌平']['昌平'] = new Array('百善镇', '北七家镇', '长陵镇', '城北街道', '城南街道', '崔村镇', '东小口地区', '回龙观地区', '流村镇', '马池口地区', '南口地区', '南邵镇', '沙河地区', '十三陵镇', '小汤山镇', '兴寿镇', '阳坊镇');
    GC3['北京']['朝阳'] = new Array();
    GC3['北京']['朝阳']['朝阳'] = new Array('安贞街道', '奥运村地区奥运村乡', '八里庄街道', '常营回族地区常营回族乡', '朝阳门外街道', '崔各庄地区崔各庄乡', '大屯街道', '东坝地区东坝乡', '东风地区东风乡', '豆各庄地区豆各庄乡', '高碑店地区高碑店乡', '管庄地区管庄乡', '和平街街道', '黑庄户地区黑庄户乡', '呼家楼街道', '建国门外街道', '将台地区将台乡', '金盏地区金盏乡', '劲松街道', '酒仙桥街道', '来广营地区来广营乡', '六里屯街道', '麦子店街道', '南磨房地区南磨房乡', '潘家园街道', '平房地区平房乡', '三间房地区三间房乡', '三里屯街道', '十八里店地区十八里店乡', '首都机场街道', '双井街道', '孙河地区孙河乡', '太阳宫地区太阳宫乡', '团结湖街道', '王四营地区王四营乡', '望京街道', '望京开发街道', '香河园街道', '小关街道', '小红门地区小红门乡', '亚运村街道', '左家庄街道', '垡头街道');
    GC3['北京']['崇文'] = new Array();
    GC3['北京']['崇文']['崇文'] = new Array('崇文门外街道', '东花市街道', '龙潭街道', '前门街道', '体育馆路街道', '天坛街道', '永定门外街道');
    GC3['北京']['大兴'] = new Array();
    GC3['北京']['大兴']['大兴'] = new Array('安定镇', '北臧村镇', '采育镇', '长子营镇', '黄村地区黄村镇', '旧宫地区旧宫镇', '礼贤镇', '林校路街道', '庞各庄镇', '青云店镇', '清源街道', '魏善庄镇', '西红门地区西红门镇', '兴丰街道', '亦庄地区亦庄镇', '榆垡镇', '瀛海镇');
    GC3['北京']['东城'] = new Array();
    GC3['北京']['东城']['东城'] = new Array('安定门街道', '北新桥街道', '朝阳门街道', '东华门街道', '东四街道', '东直门街道', '和平里街道', '建国门街道', '交道口街道', '景山街道');
    GC3['北京']['房山'] = new Array();
    GC3['北京']['房山']['房山'] = new Array('长沟镇', '长阳镇', '城关街道', '大安山乡', '大石窝镇', '东风街道', '佛子庄乡', '拱辰街道', '韩村河镇', '河北镇', '良乡地区', '琉璃河地区', '南窖乡', '蒲洼乡', '青龙湖镇', '十渡镇', '石楼镇', '史家营乡', '西潞街道', '霞云岭乡', '向阳街道', '新镇街道', '星城街道', '阎村镇', '迎风街道', '张坊镇', '周口店地区', '窦店镇');
    GC3['北京']['丰台'] = new Array();
    GC3['北京']['丰台']['丰台'] = new Array('长辛店街道', '长辛店镇', '大红门街道', '东高地街道', '东铁匠营街道', '方庄地区', '丰台街道', '和义街道', '花乡乡', '卢沟桥街道', '卢沟桥乡', '马家堡街道', '南苑街道', '南苑乡', '太平桥街道', '宛平城地区', '王佐镇', '西罗园街道', '新村街道', '右安门街道', '云岗街道');
    GC3['北京']['海淀'] = new Array();
    GC3['北京']['海淀']['海淀'] = new Array('万寿路街道', '永定路街道', '羊坊店街道', '甘家口街道', '八里庄街道', '紫竹院街道', '北下关街道', '北太平庄街道', '学院路街道', '中关村街道', '海淀街道', '青龙桥街道', '清华园街道', '燕园街道', '香山街道', '清河街道', '花园路街道', '西三旗街道', '马连洼街道', '田村路街道', '上地街道', '万柳地区（海淀乡）', '东升地区（东升乡）', '曙光街道', '温泉镇', '四季青镇', '西北旺镇', '苏家坨镇', '上庄镇');
    GC3['北京']['怀柔'] = new Array();
    GC3['北京']['怀柔']['怀柔'] = new Array('宝山镇', '北房镇', '渤海镇', '长哨营满族乡', '怀北镇', '怀柔地区', '九渡河镇', '喇叭沟门满族乡', '琉璃庙镇', '龙山街道', '庙城地区', '桥梓镇', '泉河街道', '汤河口镇', '雁栖地区', '杨宋镇');
    GC3['北京']['门头沟'] = new Array();
    GC3['北京']['门头沟']['门头沟'] = new Array('城子街道', '大台街道', '大峪街道', '东辛房街道', '军庄镇', '龙泉镇', '妙峰山镇', '清水镇', '潭柘寺镇', '王平地区', '雁翅镇', '永定镇', '斋堂镇');
    GC3['北京']['密云'] = new Array();
    GC3['北京']['密云']['密云'] = new Array('北庄镇', '不老屯镇', '大城子镇', '东邵渠镇', '冯家峪镇', '高岭镇', '鼓楼街道', '古北口镇', '果园街道', '河南寨镇', '巨各庄镇', '密云镇', '穆家峪镇', '十里堡镇', '石城镇', '太师屯镇', '檀营地区檀营满族蒙古族乡', '西田各庄镇', '溪翁庄镇', '新城子镇');
    GC3['北京']['石景山'] = new Array();
    GC3['北京']['石景山']['石景山'] = new Array('八宝山街道', '八角街道', '北辛安街道', '古城街道', '广宁街道', '金顶街街道', '老山街道', '鲁谷街道', '苹果园街道', '五里坨街道');
    GC3['北京']['顺义'] = new Array();
    GC3['北京']['顺义']['顺义'] = new Array('北石槽镇', '北务镇', '北小营镇', '大孙各庄镇', '高丽营镇', '光明街道', '后沙峪地区', '空港街道', '李桥镇', '李遂镇', '龙湾屯镇', '马坡地区', '木林镇', '南彩镇', '南法信地区', '牛栏山地区', '仁和地区', '胜利街道', '石园街道', '双丰街道', '天竺地区', '旺泉街道', '杨镇地区', '张镇', '赵全营镇');
    GC3['北京']['通州'] = new Array();
    GC3['北京']['通州']['通州'] = new Array('漷县镇', '北苑街道', '梨园地区', '潞城镇', '马驹桥镇', '宋庄镇', '台湖镇', '西集镇', '新华街道', '永乐店镇', '永顺地区', '于家务回族乡', '玉桥街道', '张家湾镇', '中仓街道');
    GC3['北京']['西城'] = new Array();
    GC3['北京']['西城']['西城'] = new Array('德胜街道', '金融街街道', '什刹海街道', '西长安街街道', '新街口街道', '月坛街道', '展览路街道');
    GC3['北京']['宣武'] = new Array();
    GC3['北京']['宣武']['宣武'] = new Array('白纸坊街道', '椿树街道', '大栅栏街道', '广安门内街道', '广安门外街道', '牛街街道', '陶然亭街道', '天桥街道');
    GC3['北京']['延庆'] = new Array();
    GC3['北京']['延庆']['延庆'] = new Array('八达岭镇', '大榆树镇', '大庄科乡', '井庄镇', '旧县镇', '康庄镇', '刘斌堡乡', '千家店镇', '沈家营镇', '四海镇', '香营乡', '延庆镇', '永宁镇', '张山营镇', '珍珠泉乡');

    return {
      /*新建地址*/
      newAddress: function(obj, addresses) {
        addresses.push(obj);
      },
      /*删除某一个地址*/
      delAddress: function(id, $scope) {
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
      /*获取默地址*/
      getDefaultAddress: function(addresses) {
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
      /*更新地址*/
      updateAddress: function(obj, addresses) {
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
      /*将某一个地址设置为默认*/
      setDefaultAddress: function(id, addresses) {
        _.each(addresses, function(item) {
          if (item.id == id) {
            item.isdefault = 1;
          } else {
            item.isdefault = 0;
          }
        });
      },
      /*通过ID得到地址信息*/
      getAddressByID: function(id, addresses) {
        var exists = _.where(addresses, {
          id: parseInt(id)
        });
        if (exists.length > 0) {
          return exists[0];
        }
        return null;
      },
      /*通过区域获得街道*/
      getCurrentStreets: function(address) {
        return _.clone(GC3[address.province][address.city][address.region]);
      },
      getCurrentRegions: function(address) {
        var a = _.clone(GC2[address.province][address.city]);
        console.log(a);
        return a;
      },
      getCurrentCities: function(address) {
        var a = _.clone(GC1[address.province]);
        console.log(a);
        return a;
      },
      /*通过区域获得街道*/
      getCurrentStreets: function(address) {
        return _.clone(GC3[address.province][address.city][address.region]);
      },
      getCurrentRegions: function(address) {
        var a = _.clone(GC2[address.province][address.city]);
        console.log(a);
        return a;
      },
      getCurrentCities: function(address) {
        var a = _.clone(GC1[address.province]);
        console.log(a);
        return a;
      },
      getProvinces: function() {
        return _.clone(GP);
      }
    }
  })
  /*
   加载框
   */
  .factory('Loading', function($ionicLoading) {
    return {
      /*显示进度框*/
      show: function(delay) {
        delay = delay || 1000;
        $ionicLoading.show({
          delay: delay
        });
      },
      /*提示文本*/
      tip: function(message, duration) {
        duration = duration || 2000;
        $ionicLoading.hide();
        $ionicLoading.show({
          template: message,
          duration: duration,
          noBackdrop: true
        });
      },
      /*关闭进度条或文本框*/
      close: function() {
        $ionicLoading.hide();
      }
    }
  })
  .factory('SearchKeywords', function($resource) {
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
      /*获取或设置常见搜索词*/
      hots: function(array) {
        if (array) {
          hots = array;
        } else {
          return hots;
        }
      },
      /*获取本地搜索记录*/
      local: function() {
        return localKeywords;
      },
      /*将某一个关键词收录到本地搜索记录*/
      add: function(keyword) {
        var idx = localKeywords.indexOf(keyword);
        if (idx >= 0) {
          localKeywords.splice(idx, 1);
        } else {
          if (localKeywords.length > 5) {
            localKeywords.splice(4, localKeywords.length - 4);
          }
        }

        localKeywords.splice(0, 0, keyword);
        localStorage.searchKeywords = angular.toJson(localKeywords);
      },
      /*清除本地搜索记录*/
      clearLocalKeyword: function() {
        localKeywords = [];
        localStorage.searchKeywords = angular.toJson(localKeywords);
      }
    }
  })
  .factory('Location', function($q) {
    return {
      current: function() {
        var deferred = $q.defer();
        var geolocation = new BMap.Geolocation();
        geolocation.getCurrentPosition(function(r) {

          if (this.getStatus() == BMAP_STATUS_SUCCESS) {
            r.x = r.longitude;
            r.y = r.latitude;
            deferred.resolve(r);
          } else {
            deferred.reject('定位失败');
          }
        }, {
          enableHighAccuracy: true
        });

        return deferred.promise;
      }
    }
  })
  .filter('mobilemask', function() {

   return function(input) {
     var result = input;
     if (result) {
       if (result.length >= 7) {
         result = result.substr(0, 3) + '****' + result.substr(7, result.length - 7);
       }
     }

     return result;
   };
 })
  /*
   http 拦截器，所有的网络请求都会先经过于此
   */
  .factory('HttpInterceptor', function($q, $rootScope) {
    var interceptor = {
      'responseError': function(rejection) {
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
      'response': function(response) {

        if (response.data && response.data.hasOwnProperty('flag')) {
          try {
            if (response.data.flag >= 1) {
              return response;
            } else {
              var message = '服务器错误';
              if (response.data.msg) {
                message = response.data.msg;
              }

              $rootScope.$broadcast('http:errorResponse', {
                message: message
              });
              return $q.reject(response);
            }
          } catch (error) {
            console.log(error);

            $rootScope.$broadcast('http:exceptionResponse', {
              message: '网络请求发生异常'
            });

            return $q.reject(response);
          }
        }

        return response;
      },
      'request': function(http) {
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
