angular.module('starter.controllers', ['ngResource', 'pasvaz.bindonce', 'base64'])

    .run(function ($rootScope, $state, $q, $ionicPopup, $ionicLoading, $resource, $http, $stateParams, $location, $ionicPlatform, $ionicHistory, $ionicModal, $window, $timeout, User, Loading) {
        $window.addEventListener('online', function () {
            $rootScope.offline = false;
            $ionicLoading.hide();
        });
        $window.addEventListener('offline', function () {
            $rootScope.offline = true;
            $ionicLoading.show({
                template: '没有网络不能操作'
            });
        });
        $rootScope.closeLogin = function () {
            $rootScope.loginModal.hide();
            //var back = $ionicHistory.backView();
            $state.transitionTo($state.current, $stateParams, {
                reload: true,
                inherit: false,
                notify: true
            });
        };
        $rootScope.changeStatus = function (status) {
            $rootScope.registerModel = {};
            $rootScope.resetPasswordModel = {};
            $rootScope.loginModalStatus = status;
        };
        $rootScope.requestCodeWithRegister = function () {
            var userName = $rootScope.registerModel.userName + '';
            if (userName.length != 11) {
                return Loading.tip('请输入正确的手机号码');
            }

            User.requestValidationCodeRegister(userName)
                .then(function (result) {
                    $rootScope.counterWithRequestCode = 60;
                    $rootScope.requestCodeProcessing = true;

                    var loop = function () {
                        if (--$rootScope.counterWithRequestCode <= 0) {
                            $rootScope.counterWithRequestCode = 60;
                            $rootScope.requestCodeProcessing = false;
                        } else {
                            $timeout(loop, 1000);
                        }
                    };

                    loop();
                })
                .catch(function (error) {
                    if (error.message) {
                        Loading.tip(error.message);
                    }
                });
        };
        $rootScope.requestCodeWithRecovery = function () {
            var userName = $rootScope.resetPasswordModel.userName + '';

            if (userName.length != 11) {
                return Loading.tip('请输入正确的手机号码');
            }

            User.requestValidationCodeRecovery(userName)
                .then(function (result) {
                    $rootScope.requestCodeProcessing = true;
                    $rootScope.counterWithRequestCode = 60;

                    var loop = function () {
                        if (--$rootScope.counterWithRequestCode <= 0) {
                            $rootScope.counterWithRequestCode = 60;
                            $rootScope.requestCodeProcessing = false;
                        } else {
                            $timeout(loop, 1000);
                        }
                    };

                    loop();
                })
                .catch(function (error) {
                    if (error.message) {
                        Loading.tip(error.message);
                    }
                });
        };
        $ionicModal
            .fromTemplateUrl('templates/login.html', {
                scope: $rootScope
            })
            .then(function (modal) {
                $rootScope.loginModal = modal;
            });
        $rootScope.loginWithQQ = function () {
            Loading.show();

            User
                .loginWithQQ()
                .then(function () {
                    Loading.close();
                    User.syncProfile();

                    $rootScope.loginModal.hide();
                })
                .catch(function (error) {
                    if (error) {
                        Loading.tip(error);
                    }
                });
        };
        $rootScope.register = function () {
            if ($rootScope.registerModel.userName && $rootScope.registerModel.password && $rootScope.registerModel.confirmPassword && $rootScope.registerModel.validationCode) {
                if ($rootScope.registerModel.password == $rootScope.registerModel.confirmPassword) {
                    Loading.show();
                    var loginHelper = $resource(config.domain + '/mobile/register');
                    loginHelper.save({
                            mobile: $rootScope.registerModel.userName,
                            password: hex_md5($rootScope.registerModel.password),
                            apassword: hex_md5($rootScope.registerModel.confirmPassword),
                            vcode: $rootScope.registerModel.validationCode,
                            referee: $rootScope.registerModel.referee
                        },
                        function (data) {
                            Loading.close();

                            if (data.flag == 1) {

                                $rootScope.loginModal.hide();
                                localStorage["username"] = $rootScope.registerModel.userName;
                                localStorage["password"] = hex_md5($rootScope.registerModel.password);
                                User.valided();
                                User.setUser(data['msg']);
                                $state.go('tab.account');
                                $rootScope.$broadcast('registSuccess');
                            } else {
                                Loading.tip(data['msg']);
                            }

                            $rootScope.registerModel.password = '';
                            $rootScope.registerModel.repassword = '';
                        },
                        function (data) {
                            Loading.tip('应用异常');
                            $rootScope.registerModel.password = '';
                            $rootScope.registerModel.confirmPassword = '';
                            console.log(data)
                        });
                } else {
                    Loading.tip('两次密码输入不一致，请重新输入');
                }
            } else {
                Loading.tip('注册信息输入不完整，请检查');
            }
        };
        $rootScope.login = function () {
            if ($rootScope.loginModel.userName && $rootScope.loginModel.password) {
                Loading.show();

                User
                    .login($rootScope.loginModel.userName, hex_md5($rootScope.loginModel.password))
                    .then(function () {
                        Loading.close();
                        User.syncProfile();

                        $rootScope.loginModalStatus = 'LOGIN';
                        $rootScope.resetPasswordModel = {};
                        $rootScope.loginModel = {};
                        $rootScope.registerModel = {};
                        $rootScope.loginModal.hide();

                        if ($rootScope.next) {
                            $state.go($rootScope.next);
                        } else {
                            $state.go('tab.account');
                        }
                    })
                    .catch(function (err) {
                        if (err && err.msg) {
                            Loading.tip(err.msg);
                        } else {
                            Loading.tip('登录失败');
                        }

                        console.log(err);
                    });
            } else {
                Loading.tip('请输入用户名和密码');
            }
        };
        $rootScope.$on('$stateChangeStart',
            function (event, toState, toParams, fromState, fromParams) {
                var validate = function () {
                        var deferred = $q.defer();
                        if (toState.validate === true && User.hasValid() === false) {
                            $rootScope.loginModel = {};
                            $rootScope.next = toState.name;
                            $rootScope.panel = 1;
                            $rootScope.loginModalStatus = 'LOGIN';
                            $rootScope.recoveryPasswordOnly = false;
                            $rootScope.loginModal.show();
                            $rootScope.next = toState.name;

                            event.preventDefault();
                            $state.go(fromState.name);
                            $rootScope.$broadcast('$stateChangeSuccess', toState, toParams, fromState, fromParams);

                            deferred.reject('账户不可用');
                        }

                        deferred.resolve();
                        return deferred.promise;
                    },
                    hideTabs = function () {
                        var deferred = $q.defer();
                        if (toState.hideTabs) {
                            $rootScope.tohide = "tabs-item-hide";
                        } else {
                            $rootScope.tohide = "";
                        }

                        deferred.resolve();
                        return deferred.promise;
                    },
                    networkDetect = function () {
                        var deferred = $q.defer();

                        if ($rootScope.offline) {
                            event.preventDefault();
                            $rootScope.$broadcast('$stateChangeSuccess', toState, toParams, fromState, fromParams);

                            deferred.reject('离线不可用');
                        }

                        deferred.resolve();
                        return deferred.promise;
                    };

                networkDetect()
                    .then(validate)
                    .then(hideTabs)
                    .catch(function (err) {
                        console.log(err);
                    });
            }
        );
        $rootScope.$on('user:requireLogin', function (event, args) {
            Loading.tip('请您登录');
            $rootScope.loginModal.show();
            // $rootScope.loginDeferred = args.deferred;
            $rootScope.recoveryPasswordOnly = false;
        });
        $rootScope.validateCode = function () {
            if (!$rootScope.resetPasswordModel.userName) {
                return Loading.tip('请输入手机号码');
            }

            if (!$rootScope.resetPasswordModel.validationCode) {
                return Loading.tip('请输入验证码 ');
            }

            User.requestResetPassword($rootScope.resetPasswordModel.validationCode, $rootScope.resetPasswordModel.userName)
                .then(function (result) {
                    var userName = $rootScope.resetPasswordModel.userName;
                    $rootScope.changeStatus('RESETPASSWORD');
                    $rootScope.resetPasswordModel.userName = userName;
                })
                .catch(function (error) {
                    Loading.tip(error.message);
                });
        };
        $rootScope.resetPassword = function () {
            var user = User.current(),
                userName = $rootScope.resetPasswordModel.userName,
                password = $rootScope.resetPasswordModel.password,
                confirm = $rootScope.resetPasswordModel.confirmPassword;

            if (password.length === 0) {
                return Loading.tip('密码不能为空');
            }

            if (password !== confirm) {
                return Loading.tip('密码与确认密码不一致，请重新输入');
            }

            User
                .resetPassword(userName, password)
                .then(function (result) {
                    Loading.tip('您的密码已修改');
                    $rootScope.resetPasswordModel = {};
                    $rootScope.loginModal.hide();
                    $rootScope.changeStatus('LOGIN');
                    $state.go('tab.account');
                })
                .catch(function (error) {
                    Loading.tip(error.message);
                });
        };
        $rootScope.recoverPassword = function () {
            $rootScope.loginModalStatus = 'RECOVERPASSWORD';
        };
        $ionicPlatform.ready(function () {

            var setTagsWithJPush = function (tags, alias) {
                if (window.plugins && window.plugins.jPushPlugin) {
                    window.plugins.jPushPlugin.setTagsWithAlias(tags, alias);
                }
            };

            $rootScope.$on('loginSuccess',
                function (event, user) {
                    var tags = ['user'],
                        alias = user.msg.mobile;

                    if (user.mobile == '13239109398') {
                        tags.push('administrator');
                    }

                    setTagsWithJPush(tags, alias);
                });

            if (window.plugins && window.plugins.jPushPlugin) {
                window.plugins.jPushPlugin.init();
            }
        });

        User.loginBackend();
        $rootScope.loginModalStatus = 'LOGIN';
        $rootScope.resetPasswordModel = {};
        $rootScope.loginModel = {};
        $rootScope.registerModel = {};
        Map.scope = $rootScope;
    })
    /*
     添加评论路由
     */
    .controller('CommentCtrl', function ($http, $resource, $scope, $http, $state, $ionicHistory, Loading, User) {
        var psid = $state.params.psid,
            oiid = $state.params.oiid;

        Loading.close();
        $scope.comment = {
            productRate: 0,
            speedRate: 0,
            priceRate: 0,
            serviceRate: 0,
            psid: psid,
            oiid: oiid,
            userId: User.current().id
        };
        $scope.rateProduct = function (rate) {
            $scope.comment.productRate = rate;
        }
        $scope.rateSpeed = function (rate) {
            $scope.comment.speedRate = rate;
        };
        $scope.ratePrice = function (rate) {
            $scope.comment.priceRate = rate;
        }
        $scope.rateService = function (rate) {
            $scope.comment.serviceRate = rate;
        }
        $scope.save = function () {
            var comment = $scope.comment;
            if (!comment.content) {
                return Loading.tip('请填些评价内容', 1200);
            }

            var resource = $resource(config.domain + '/mobile/comment/add');
            resource.save(comment,
                function () {
                    Loading.tip('您已评价，谢谢');
                    var user = User.current();
                    var resource = $resource(config.domain + '/mobile/payinfo');

                    resource.get({
                            userid: user.id,
                            price: -1
                        },
                        function (result) {
                            user.addresses = result.address;
                            user.balance = result.balance;
                            user.score = result.score;
                        },
                        function (error) {
                            console.log(error);
                        });

                    $scope.$root.$broadcast('comment', {
                        comment: comment
                    });
                    $ionicHistory.goBack();
                },
                function () {
                    Loading.tip('应用发生异常');
                    console.log(result);
                });
        };
    })
    /*
     评论列表路由
     */
    .controller('CommentsCtrl', function ($http, $resource, $scope, $state, $ionicScrollDelegate, User, Loading) {
        var refresh = function () {
            var resource = $resource(config.domain + '/mobile/comment/list');
            resource.get({
                    userId: $scope.userId,
                    psid: $scope.psid,
                    index: $scope.index,
                    size: $scope.size
                },
                function (result) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    if (result) {
                        if (result.items && result.items.length > 0) {
                            $scope.index++;

                            if ($scope.comment) {
                                result.items = _.union(result.items, $scope.comment.items);
                            }

                            $scope.comment = result;
                            $ionicScrollDelegate.resize();
                            $scope.hasMore = true;

                            return;
                        }
                    }

                    $scope.hasMore = false;
                },
                function (err) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    console.log(err);
                });

        };

        $scope.index = $scope.index || 1;
        $scope.size = $scope.size || 20;
        $scope.psid = $state.params.psid;
        $scope.load = function () {
            refresh();
        };
        $scope.hasMore = true;
    })
    /*首页control*/
    .controller('HomeCtrl', function ($scope, $resource, $state, $ionicPopup, $ionicListDelegate, $window, $filter, $timeout, $http, $location, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $ionicScrollDelegate, $q, Ad, Products, Loading, SearchKeywords, User, ShopCar) {
        var countdownWithSeckill = function (items, serverTime) {
                var currentTime = serverTime;

                $scope.interval = setInterval(function () {
                    _.each(items, function (item) {
                        if (currentTime < item.starttime) {
                            $scope.$apply(function () {
                                item.progress = '马上开始';
                                item.times = "<span>" + $filter('date')(item.starttime * 1000, 'MM月dd日HH点') + ' 后开始预售'+"</span>";
                                item.nostart = true;
                            });

                        } else if (currentTime >= item.starttime && currentTime < item.endtime) {
                            //item.progress = '进行中';
                            //item.times = $filter('date')(item.endtime * 1000, 'MM月dd日HH点') + ' 后停止预售';
                            var difference = item.endtime - currentTime;
                            var ts = paddingTime(parseInt(difference * 1000)); //计算剩余的毫秒数
                            var dd = paddingTime(parseInt(ts / 1000 / 60 / 60 / 24, 10)); //计算剩余的天数
                            var hh = paddingTime(parseInt(ts / 1000 / 60 / 60 % 24, 10)); //计算剩余的小时数
                            var mm = paddingTime(parseInt(ts / 1000 / 60 % 60, 10)); //计算剩余的分钟数
                            var ss = paddingTime(parseInt(ts / 1000 % 60, 10)); //计算剩余的秒数
                            var str = '';
                            if (dd > 0)
                                str += "<i class='assertive'>"+dd + "</i>天";
                            if (hh > 0)
                                str +="<i class='assertive'>"+ hh + "</i>小时";
                            if (mm > 0)
                                str += "<i class='assertive'>"+mm + "</i>小分";
                            if (ss <= 0)
                                str +=  "<i class='assertive'>"+ss+ "</i>00秒";
                            else
                                str += "<i class='assertive'>"+ss + "</i>秒";

                            $scope.$apply(function () {
                                item.times = '<span>剩余'+str+'</span>';
                            });

                        } else if (currentTime >= item.endtime) {
                            $scope.$apply(function () {
                                item.progress = '已结束';
                                item.times = '<span>已结束</span>';
                                item.nostart = true;
                            });
                        }
                    });
                    currentTime += 1;
                }, 1000);
            },
            paddingTime = function checkTime(i) {
                if (i < 10) {
                    i = " " + i;
                }
                return i;
            },
            fetchAds = function () {
                var deferred = $q.defer();
                var ads = [];

                Ad
                    .refresh()
                    .then(function (result) {
                        ads = result;
                        $scope.loading = true;
                        $timeout(function () {
                            $scope.ads = ads;
                            var handler = $ionicSlideBoxDelegate.$getByHandle('slide-ads');

                            if (handler) {
                                handler.update();
                            }
                            $scope.loading = false;
                        }, 1000);

                        deferred.resolve();
                    })
                    .catch(function (error) {
                        //如果获取广告失败，依然通过
                        deferred.resolve();
                    });

                return deferred.promise;
            },
            fetchProducts = function () {
                var deferred = $q.defer();

                Products
                    .refresh()
                    .then(function (result) {

                        $scope.fruits = result.fruits;
                        $scope.vegetables = result.vegetables;
                        $scope.trades = result.trades;
                        $scope.bargains = result.bargains;
                        $scope.pre_sales = result.pre_sales;
                        //$scope.buying = result.buying;
                        countdownWithSeckill(result.pre_sales, result.time);
                        $scope.titleClick('BARGAINS');
                        SearchKeywords.hots(result.hots);
                        deferred.resolve();
                    })
                    .catch(function (error) {
                        deferred.reject('应用异常');
                    });

                return deferred.promise;
            };

        $scope.$root.$on('loginSuccess', function () {
            var user = User.current();
            if (user) {
                $scope.score = user.score
            } else {
                $scope.score = null;
            }
        });
        $scope.$root.$on('user:tradeSuccess', function (event, args) {
            $scope.score = args.user.score;
        });
        $scope.$on('$ionicView.afterEnter', function () {
            $ionicSlideBoxDelegate.$getByHandle('slide-ads').update();
        });
        $scope.$root.$on('store:clearDefaultSuccess', function () {
            $timeout(function () {
                localStorage.storeID = localStorage.storeName = '';
            }, 1500);
        });

        $scope.showDetail = function (id) {
            var extra = 'NORMAL';
            if ($scope.display === 'TRADE') {
                extra = 'TRADE';
            }

            $state.go($state.$current.name + '-product', {
                id: id,
                extra: extra
            });
        };
        $scope.titleClick = function (type) {
            $ionicScrollDelegate.resize();
            if ($scope.display != type) {
                switch (type) {
                    //case 'm':
                    //    $scope.items = $scope.seckill;
                    //   break;
                    case 'BARGAINS':
                        $scope.items = $scope.bargains;
                        break;
                    case 'TRADE':
                        $scope.items = $scope.trades;
                        break;
                    case 'PRESALES':
                        $scope.items = $scope.pre_sales;
                        break;
                    case 'RECOMMAND':
                        //$scope.items = $scope.vegetables;
                        break;
                    case 'FRUITE':
                        $scope.items = $scope.fruits;
                        break;
                    //case 'BUYING':
                    //    $scope.items = $scope.pre_sales;
                    //    break;
                }

                $scope.display = type;
            }
        };
        $scope.search = function () {
            $state.go('tab.search');
        };
        $scope.docker = function (id) {
            var ad = Ad.get(id);
            if (ad) {
                switch (ad.href.key) {
                    case '1':
                        $state.go($state.$current.name + '-product', {
                            id: ad.href.value
                        });
                        break;

                    case '2':
                        $scope.goCategoriesView(ad.href.value);
                        break;

                    case '3':
                        if (ad.href.value) {
                            window.open(ad.href.value, '_blank');
                        }
                        break;

                    case '4':
                        var exist = _.find($scope.pre_sales, function (item) {
                            return (item.id === parseInt(ad.href.value));
                        });

                        if (exist) {
                            ShopCar.setPresaleForDetail(exist);
                            $state.go('tab.pre-sale-detail');
                        }
                        break;
                }
            }
        };
        //$scope.showPresaleRule = function (id) {
        //    $scope.presaleRuleID = parseInt(id);
        //    $ionicScrollDelegate.resize();
        //};
        $scope.goCategoriesView = function (selectCategoryCode) {
            $state.go('tab.categories', {});
            $timeout(function () {
                $scope.$root.$broadcast('requireChangeCategory', {
                    code: selectCategoryCode
                });
            }, 500);
        };
        $scope.refresh = function (shouldNotLoading) {
            if ($scope.interval) {
                clearInterval($scope.interval);
            }

            if (!shouldNotLoading) {
                Loading.show();
            }

            $q
                .all([fetchAds(), fetchProducts()])
                .then(function () {
                    $scope.$broadcast('scroll.refreshComplete');
                    Loading.close();
                });
        };
        $scope.nearby = function () {
            if (localStorage.storeID && localStorage.storeName) {
                $state.go('tab.home-store-categories', {
                    from: 'tab.home'
                });
            } else {
                Loading.tip('请选择最近的门店');
                $state.go('tab.home-nearby', {
                    from: 'tab.home'
                });
            }
        };
        $scope.showPresaleDetail = function (id) {
            var exist = _.find($scope.pre_sales, function (item) {
                return (item.id === parseInt(id));
            });

            if (exist) {
                ShopCar.setPresaleForDetail(exist);
                $state.go('tab.pre-sale-detail');
            }
        };
        $scope.refresh();
    })
    /*产品详情页control*/
    .controller('ProductCtrl', function ($scope, $resource, $state, $window, $location, $ionicPopup, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {
        var fetchProduct = function () {
            var resources = $resource(config.domain + '/mobile/product/' + $state.params.id),
                user = User.current();

            Loading.show();
            resources.get(
                function (product) {
                    if (product.status === 1) {
                        Loading.close();
                        product.pics = _.map(product.pics, function (item) {
                            item.img = config.domain + '/upload/' + product.sku + '/' + item.img;
                            return item;
                        });
                        $scope.product = product;
                        $scope.product.limit = product.xgperusernum || 0;
                        $scope.product.renaming = product.xgtotalnum || 0;
                        $scope.favorite = Favorite.contains(product.psid);
                        $scope.standards = product.standards;
                        $scope.setStandard(product.psid);
                        $ionicSlideBoxDelegate.update();
                    } else {
                        $ionicHistory.goBack();
                        Loading.tip('抱歉,该商品暂时不可用或已下架');
                    }
                },
                function (data) {
                    Loading.tip('应用异常');
                    console.log(data);
                });
        };
        $scope.cancelFavorite = function (id) {
            var userId = null,
                user = User.current();

            if (user) {
                userId = user.id;
            }

            Favorite.remove(userId, id);
            Loading.tip('已取消收藏', 1000);
        };
        $scope.doFavorite = function (id) {
            if ($scope.favorite) {
                $scope.cancelFavorite(id);
            } else {
                $scope.favoriteProduct(id);
            }

            $scope.favorite = !$scope.favorite;

        };
        $scope.favoriteProduct = function (id) {
            var userId = null,
                user = User.current();

            if (user) {
                userId = user.id;
            }

            Favorite.add(userId, id);
            Loading.tip('已收藏', 1000);
        };
        $scope.trade = function () {
            var user = User.current(),
                resource = $resource(config.domain + '/mobile/score_buy');

            if (!user) {
                return $scope.$emit('user:requireLogin');
            }

            resource.save(
                {
                    userid: user.id,
                    psid: $scope.product.psid,
                    quantity: $scope.quantity
                }, function (result) {
                    if (result) {
                        if (result.flag != 1) {
                            return Loading.tip(result.msg || '错误');
                        }
                        user.score -= $scope.product.score;
                        $scope.$root.$broadcast('user:tradeSuccess', {
                            user: user
                        });

                        Loading.tip('已换购成功, 请到购物车提交');
                    } else {
                        Loading.tip('服务器无响应');
                    }
                }, function (error) {
                    Loading.tip('应用异常');
                    console.log(data);
                }
            );
        };
        $scope.buy = function () {
            var resource = $resource(config.domain + '/mobile/shopcar'),
                user = User.current();

            Loading.show();
            resource.query({
                psid: '[' + $scope.chooseStandard.psid + ']'
            }, function (products) {
                Loading.close();
                _.each(products, function (product) {

                    var quantity = $scope.quantity;
                    var cars = ShopCar.all();
                    var exist = _.find(cars, function (car) {
                        return car.pid === $scope.chooseStandard.pid && car.psid === $scope.chooseStandard.psid;
                    });

                    if (exist) {
                        quantity += exist.quantity;
                    }

                    var newProduct = {
                        pid: $scope.chooseStandard.pid,
                        psid: $scope.chooseStandard.psid,
                        quantity: quantity,
                        product: product,
                        checked: true,
                        limit: $scope.product.limit,
                        renaming: $scope.product.renaming
                    };

                    if (user) {
                        var checkQuantityResource = $resource(config.domain + '/mobile/check_cart');
                        checkQuantityResource.get({
                            uid: user.id,
                            psid: $scope.chooseStandard.psid,
                            pid: $scope.chooseStandard.pid,
                            quantity: quantity
                        }, function (result) {
                            if (result && result.flag === 1) {
                                ShopCar.put(newProduct);
                                if (user) {
                                    ShopCar.upload(user.id, ShopCar.all());
                                }

                                Loading.tip('已加入到购物车', 1000);
                                return;
                            }

                            if (result.count < 0) {
                                result.count = 0;
                            }

                            Loading.tip(result.msg);
                        }, function (error) {

                            Loading.close();
                        });
                    } else {
                        ShopCar.put(newProduct);
                        if (user) {
                            ShopCar.upload(user.id, ShopCar.all());
                        }

                        Loading.tip('已加入到购物车', 1000);
                    }

                });
            }, function (error) {
                Loading.tip('应用异常');
                console.log(error);
            });

        };
        $scope.addQuantity = function (num) {
            var user = User.current(),
                resource = $resource(config.domain + '/mobile/check_cart');

            var quantity = $scope.quantity + num;

            if (quantity < 1) {
                quantity = 1;
            }

            if ($scope.product.renaming && $scope.product.renaming > 0 && quantity > $scope.product.renaming) {
                Loading.tip('抱歉，库存不足');
                return;
            }

            if ($scope.product.limit && $scope.product.limit > 0 && quantity > $scope.product.limit) {
                Loading.tip('抱歉，当前商品最多可购买' + $scope.product.limit + '份');
                return;
            }

            Loading.show();
            if (user) {
                resource.get({
                    uid: user.id,
                    psid: $scope.product.psid,
                    pid: $scope.product.pid,
                    quantity: quantity
                }, function (result) {
                    if (result && result.flag === 1) {
                        $scope.quantity = quantity;
                        return Loading.close();
                    }

                    if (result.count < 0) {
                        result.count = 0;
                    }

                    $scope.quantity = result.count;
                    Loading.tip(result.msg);
                }, function (error) {
                    Loading.close();
                });
            } else {
                $scope.quantity = quantity;
            }

        };
        $scope.showDetail = function () {
            $state.go($state.current.name + '-detail', {
                id: $scope.product.psid
            });
        };
        $scope.setStandard = function (psid) {
            $scope.chooseStandard = _.find($scope.standards, function (standard) {
                return standard.psid === parseInt(psid);
            });
        };
        $scope.showComments = function (psid) {
            $state.go($state.$current.name + '-comments', {
                psid: $scope.product.psid
            });
        };

        $scope.share = function (psid) {
            var title = '新鲜' + $scope.product.name + '只需' + $scope.product.price + ' 元,只在车装甲',
                url = 'http://www.eofan.com/product/' + psid;

            $window.plugins.socialsharing.share(title, null, null, url);
        };
        $scope.extra = $state.params.extra || 'NORMAL';
        $scope.chooseCopies = 0;
        $scope.favorite = true;
        $scope.quantity = 1;

        fetchProduct();
    })

    .controller('StoreProductCtrl', function ($scope, $resource, $state, $window, $location, $ionicPopup, $ionicScrollDelegate, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {

        var storeID = $state.params.storeID || localStorage.storeID,
            fetchProduct = function () {
                var resources = $resource(config.domain + '/mobile/store_product/' + $state.params.id + '?sid=' + storeID),
                    user = User.current();

                Loading.show();
                resources.get(
                    function (product) {
                        if (product.status === 1) {
                            Loading.close();
                            product.pics = _.map(product.pics, function (item) {
                                item.img = config.domain + '/upload/' + product.sku + '/' + item.img;
                                return item;
                            });
                            $scope.product = product;
                            $scope.product.limit = product.xgperusernum || 0;
                            $scope.product.renaming = product.xgtotalnum || 0;
                            $scope.favorite = Favorite.contains(product.psid);
                            //$scope.standards = product.standards;
                            $scope.copies = product.standards;
                            $ionicSlideBoxDelegate.update();
                        } else {
                            $ionicHistory.goBack();
                            Loading.tip('抱歉,该商品暂时不可用或已下架');
                        }
                    },
                    function (data) {
                        Loading.tip('应用异常');
                        console.log(data);
                    });
            };

        $scope.closeCopies = function () {
            $scope.status = 'SUMMARY';
            $ionicScrollDelegate.scrollTop();
        };
        $scope.buy = function () {
            var user = User.current(),
                checked = _.where($scope.copies, {checked: true}),
                checkQuantityResource = $resource(config.domain + '/mobile/check_cart'),
                counter = 0,
                hasError = false,
                successCount = 0,
                all = checked.length,
                onFinish = function () {
                    if (counter >= all) {
                        if (user) {
                            ShopCar.upload(user.id, ShopCar.all());
                        }

                        if (hasError) {
                            if (successCount > 0) {
                                Loading.tip('部分商品已加入到购物车', 1000);
                            } else {
                                Loading.tip('购买失败', 1000);
                            }

                        } else {
                            $scope.status = 'SUMMARY';
                            Loading.tip('已加入到购物车', 1000);
                        }
                    }
                };

            if (user) {
                _.each(checked, function (copie) {
                    var newProduct = {
                        poid: copie.poid,
                        pid: copie.pid,
                        psid: copie.psid,
                        quantity: 1,
                        product: $scope.product,
                        checked: true,
                        type: 3
                    };
                    counter++;
                    checkQuantityResource.get({
                        uid: 0,
                        psid: copie.psid,
                        pid: copie.pid,
                        poid: copie.poid,
                        quantity: 1
                    }, function (result) {
                        if (result && result.flag === 1) {
                            ShopCar.put(newProduct);
                            successCount++;
                        } else {
                            hasError = true;
                        }

                        copie.error = result.msg;
                        copie.checked = false;

                        onFinish();
                    }, function (error) {
                        copie.error = '购买失败';
                        onFinish();
                        console.log(error);
                    });
                });
            } else {
                $scope.$root.next = $state.$current.name;
                $scope.$emit('user:requireLogin');
                $scope.status = 'SUMMARY';
            }
        };
        $scope.showCopies = function () {

            $scope.status = 'DETAIL';
            $ionicScrollDelegate.resize();
        };
        $scope.showDetail = function () {
            $state.go($state.current.name + '-detail', {
                id: $scope.product.psid
            });
        };
        $scope.chooseCopie = function (id) {
            var exists = _.find($scope.copies, function (copie) {
                return copie.poid === parseInt(id);
            });

            if (exists) {
                exists.checked = !exists.checked;
                exists.error = '';
                $scope.resumeWithCopies();
            }
        };
        $scope.resumeWithCopies = function () {
            var checked = _.where($scope.copies, {checked: true});
            var resume = 0;
            _.each(checked, function (item) {
                resume += item.price;
            });

            $scope.resumeForCopies = parseFloat($filter('number')(resume, 2));
            $scope.chooseCopies = checked.length;
        };
        $scope.showComments = function (psid) {
            $state.go($state.$current.name + '-comments', {
                psid: $scope.product.psid
            });
        };
        $scope.share = function (psid) {
            var title = '新鲜' + $scope.product.name + '只需' + $scope.product.price + ' 元,只在车装甲',
                url = 'http://www.eofan.com/product/' + psid;

            $window.plugins.socialsharing.share(title, null, null, url);
        };
        $scope.chooseCopies = 0;
        $scope.status = 'SUMMARY';

        fetchProduct();
    })
    /*产品图片详情页control*/
    .controller('PDetailCtrl', function ($scope, $resource, $state, Loading) {
        var productHelper = $resource(config.domain + '/mobile/pdetail/' + $state.params.id);
        Loading.show();
        productHelper.query(
            function (pics) {
                Loading.close();
                $scope.pics = _.map(pics, function (item) {
                    item.img = config.domain + '/upload/' + item.img;
                    return item;
                });
            },
            function (data) {
                Loading.close();
                Loading.tip('应用异常');
                console.log(data)
            });
    })
    /*
     *分类查找产品control
     */
    .controller('CategoriesCtrl', function ($scope, $resource, $state, $ionicScrollDelegate, $location, $timeout, Loading) {
        Loading.show();
        var categoryHelper = $resource(config.domain + '/mobile/category');
        categoryHelper.query(
            function (data) {
                Loading.close();
                $scope.categories = data;

                if (data && data.length > 0) {
                    var choose = _.find(data, function (item) {
                        return item.code == "'" + $state.params.selected + "'";
                    });

                    if (!choose) {
                        choose = _.find(data, function (item) {
                            return (item && item.code && item.code.length === 4);
                        });
                    }

                    if (!choose) {
                        choose = {
                            name: '全部',
                            code: ''
                        };
                    }

                    $scope.choose = choose.name;
                    $scope.showProduct(choose.code.replace(/'/g, ""), choose.name);
                }
            },
            function (data) {
                Loading.tip('应用异常');
                console.log(data)
            });

        var productHelper = $resource(config.domain + '/mobile/products');
        $scope.showProduct = function (code, name) {
            $location.hash(code);
            $timeout(function () {
                $ionicScrollDelegate.$getByHandle('categoriesNameScroll').anchorScroll(code);
                $ionicScrollDelegate.$getByHandle('categoriesProductScroll').scrollTop();
            }, 1000);

            Loading.show();
            $scope.choose = name;
            productHelper.query({
                    code: code.replace('\'', '').replace('\'', '')
                },
                function (result) {
                    Loading.close();
                    $scope.products = result;
                },
                function (error) {
                    Loading.tip('应用异常');
                    console.log(error);
                });
        };
        $scope.nearby = function () {
            if (localStorage.storeID && localStorage.storeName) {
                $state.go('tab.categories-store-categories', {
                    from: 'tab.categories'
                });
            } else {
                Loading.tip('请选择最近的门店');
                $state.go('tab.categories-nearby', {
                    from: 'tab.categories'
                });
            }
        };
        $scope.showDetail = function (id) {
            $state.go($state.$current.name + '-product', {
                id: id
            });
        };
        $scope.$on('requireChangeCategory', function (event, args) {
            var exists = _.find($scope.categories, function (category) {
                return category.code == "'" + args.code + "'";
            });

            if (exists) {
                $scope.showProduct(exists.code, exists.name);
            }
        });
        $scope.config = config;
    })
    /*
     * 查找control
     */
    .controller('SearchCtrl', function ($scope, $state, $resource, Loading, SearchKeywords) {
        $scope.keyword = '';
        $scope.searchProduct = function () {
            if ($scope.keyword.length > 0) {
                SearchKeywords.add($scope.keyword);
                $state.go('tab.search-result', {
                    keyword: $scope.keyword
                });
            } else {
                Loading.tip('请输入搜索关键词', 1000);
            }
        };
        $scope.setKeyword = function (keyword) {
            $scope.keyword = keyword;
            $scope.searchProduct();
        };
        $scope.clearLocalKeyword = function () {
            SearchKeywords.clearLocalKeyword();
            $scope.keywords = SearchKeywords.local();
        };
        $scope.keywords = SearchKeywords.local();
        $scope.hots = SearchKeywords.hots();
    })
    /*用户中心control*/
    .controller('AccountCtrl', function ($scope, $state, $resource, $http, $ionicPopup, $base64, Loading, User) {
        $scope.checkin = function () {
            $scope.CHECKSTATUS = 'CHECKING';
            $http
                .post(config.domain + '/mobile/checkin', {
                    userid: User.current().id
                })
                .success(function (result) {
                    if (result.flag == 1 || result.flag == 2) {
                        $scope.CHECKSTATUS = 'CHECKED';
                        $scope.checkDays = result.seriesnum;
                        $scope.totalScore = result.totalscore;
                        $scope.scoreNumber = result.scorenum;
                        $scope.user = User.current();
                        $scope.user.score = result.totalscore;
                        if (result.flag == 1) {
                            Loading.tip('签到成功, 获得' + result.scorenum + '积分');
                        }
                    } else {
                        $scope.CHECKSTATUS = 'UNCHECKED';
                        return Loading.tip(result.error || '发生错误');
                    }
                })
                .error(function (error) {
                    $scope.CHECKSTATUS = 'UNCHECKED';
                    console.log(error);
                    Loading.tip('网络或服务器异常');
                });
        };
        $scope.logout = function () {
            var confirmPopup = $ionicPopup.confirm({
                title: '您确定要退出车装甲吗？',
                cancelText: '取消',
                okText: '确定'
            });

            confirmPopup.then(function (res) {
                if (res) {
                    User.logout();
                    $scope.$root.loginModalStatus = 'LOGIN';
                    $scope.$root.resetPasswordModel = {};
                    $scope.$root.loginModel = {};
                    $scope.$root.registerModel = {};
                    $state.go('tab.home');
                }
            });
        };
        $scope.buyWithPhone = function () {
            $ionicPopup.confirm({
                title: '通过在线支付方式购买更优惠，您确定继续拨打400电话进行订购吗？',
                cancelText: '取消',
                okText: '继续拨打'
            }).then(function (res) {
                if (res) {
                    window.open('tel:4009676558', '_self');
                }
            });
        };
        $scope.resetPassword = function () {
            var user = User.current();
            $scope.$root.resetPasswordModel.userName = user.mobile;
            $scope.$root.loginModalStatus = 'RECOVERPASSWORD';
            $scope.$root.recoveryPasswordOnly = true;
            $scope.$root.loginModal.show();

        };
        $scope.$on('loginSuccess', function (event, args) {
            $scope.user = User.current();
            if ($scope.user.hascheckedin && $scope.user.hascheckedin > 0) {
                $scope.CHECKSTATUS = 'CHECKED';
                $scope.checkDays = $scope.user.hascheckedin;
            } else {
                $scope.CHECKSTATUS = 'UNCHECKED';
            }
        });
        $scope.$on('registSuccess', function (event, args) {
            //$scope.$apply(function () {
            //    $scope.user = User.current();
            //});
            $scope.user = User.current();
            if ($scope.user.hascheckedin && $scope.user.hascheckedin > 0) {
                $scope.CHECKSTATUS = 'CHECKED';
                $scope.checkDays = $scope.user.hascheckedin;
            } else {
                $scope.CHECKSTATUS = 'UNCHECKED';
            }
        });
        $scope.user = User.current();
        $scope.config = config;
        $scope.invite = function () {
            $state.go('tab.invite');
        };
        $scope.$on('$ionicView.afterEnter', function () {
            var user = User.current();
            var resource = $resource(config.domain + '/mobile/payinfo');

            resource.get({
                    userid: user.id,
                    price: -1
                },
                function (result) {
                    if (result.hascheckedin && result.hascheckedin > 0) {
                        $scope.CHECKSTATUS = 'CHECKED';
                        $scope.checkDays = result.hascheckedin;
                    } else {
                        $scope.CHECKSTATUS = 'UNCHECKED';
                    }
                },
                function (error) {
                    console.log(error);
                });
        });

        if ($scope.user.hascheckedin && $scope.user.hascheckedin > 0) {
            $scope.CHECKSTATUS = 'CHECKED';
            $scope.checkDays = $scope.user.hascheckedin;
        } else {
            $scope.CHECKSTATUS = 'UNCHECKED';
        }
    })
    .controller('ResetPassword', function ($scope, $state, $http, $ionicHistory, Loading, User) {
        // $scope.WithRegister
        var user = User.current();
        $scope.save = function () {
            if ($scope.newPassword !== $scope.confirmPassword) {
                return Loading.tip('两次密码不一致, 请重新输入');
            }

            Loading.show();

            User
                .resetPassword($scope.mobile, $scope.newPassword)
                .success(function (result) {
                    Loading.tip('密码已修改');
                })
                .error(function (error) {
                    console.log(error);
                    Loading.tip(error.message);
                });
        };

        $scope.newPassword = $scope.mobile = '';
    })
    .controller('BindMobileCtrl', function ($scope, $state, $http, Loading, User) {
        // $scope.WithRegister
        $scope.requestValidateCode = function () {
            $scope.requestCodeProcessing = true;
            User
                .requestValidationCodeModify()
                .then(function (result) {
                    $scope.counterWithRequestCode = 60;

                    var loop = function () {
                        if (--$scope.counterWithRequestCode <= 0) {
                            $scope.counterWithRequestCode = 60;
                            $scope.requestCodeProcessing = false;
                        } else {
                            $timeout(loop, 1000);
                        }
                    };

                    loop();
                })
                .catch(function (error) {
                    $scope.requestCodeProcessing = false;
                    Loading.tip(error.message);
                });
        };

        $scope.save = function () {
            if (!$scope.validationCode) {
                return Loading.message('请输入验证码');
            }

            if (!$scope.mobile) {
                return Loading.message('请输入手机号');
            }

            $http
                .post(config.domain + '/mobile/bindmobile', {
                    mobile: $scope.mobile,
                    vcode: $scope.validationCode
                })
                .then(function (result) {
                    if (result && result.flag == 1) {
                        return $state.go('tab.reset-password');
                    } else {
                        Loading.tip(result.msg);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    Loading.tip('网络或服务器异常');
                });
        };

        $scope.validationCode = $scope.mobile = '';
    })
    /*我的订单control*/
    .controller('OrderCtrl', function ($scope, $state, $resource, $ionicScrollDelegate, User, MyOrders, Loading) {
        var query = function (type) {
            MyOrders
                .query(User.current().id, $scope.index, $scope.size, type).$promise
                .then(function (result) {

                    $scope.count = result.items.length;
                    if (result && result.items.length > 0) {
                        $scope.orders = _.union($scope.orders, result.items);
                        $scope.total = result.total;
                        $scope.index += 1;
                        switch ($scope.choose) {
                            case 'unpay':
                                $scope.hasMore = _.where(result.items, {
                                    status: '待付款'
                                }).length > 0;
                                break;

                            case 'success':
                                $scope.hasMore = _.where(result.items, {
                                    status: '交易完成'
                                }).length > 0;
                                break;
                        }

                        $ionicScrollDelegate.resize();
                        $scope.$broadcast('scroll.infiniteScrollComplete');
                    } else {
                        $scope.hasMore = false;
                        $scope.total = 0;
                    }
                }, function (error) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    Loading.tip('应用异常');
                    console.log(error);
                });
        };

        $scope.load = function () {
            query($scope.choose || 'all', $scope.index || 'indexOfAll');
        };
        $scope.switch = function (choose) {
            $scope.hasMore = true;
            $scope.orders = [];
            $scope.choose = choose;
            $scope.index = 1;
            $scope.hasMore = true;
            $ionicScrollDelegate.scrollTop();
            //switch (choose) {
            //    case 'all':
            //        query(choose);
            //        break;
            //
            //    case 'unpay':
            //        query(choose);
            //        break;
            //
            //    case 'success':
            //        query(choose);
            //        break;
            //
            //}


        };
        $scope.showDetail = function (oid, status) {
            $state.go('tab.order-detail', {
                id: oid
            });
        };
        $scope.$root.$on('cancelOrder', function (event, args) {
            var exists = _.filter($scope.orders, function (order) {
                return order.id == args.id;
            });

            if (exists && exists.length > 0) {
                var exist = exists[0];
                exist.status = '已取消';
            }
        });
        $scope.$root.$on('order:fetchSuccess', function (event, args) {
            if (args.order) {
                $scope.orders = _.map($scope.orders, function (order) {
                    if (order.id === args.order.id) {
                        return args.order;
                    }

                    return order;
                });
            }
        });
        $scope.index = 1;
        $scope.choose = 'all';
        $scope.hasMore = true;
    })
    /*继续支付*/
    .controller('ContinuePayCtrl', function ($scope, $state, $resource, $http, $q, $ionicHistory, $filter, $ionicPopup, AliPay, User, Loading) {
        var id = $state.params.id,
            alipayFinishCallback = function (args) {
                Loading.show(1);
                $http
                    .get(config.domain + '/mobile/order/status?orderid=' + args.ono)
                    .success(function (result) {
                        if (result) {
                            if (result.flag == 1) {
                                Loading.tip('您已支付成功');
                            } else {
                                Loading.tip('没有支付成功');
                            }
                        } else {
                            Loading.tip('支付存在问题, 请到 我的订单 中确认');
                        }

                        $state.go('tab.order');
                        $ionicHistory.clearHistory();
                    })
                    .catch(function (error) {
                        Loading.tip('网络或服务器出现错误');
                        $ionicHistory.goBack();
                        //$state.go('tab.order');
                        //$ionicHistory.clearHistory();
                    });
            },
            checkTimeRange = function () {
                var now = new Date(),
                    result = 4,
                    hour = now.getHours() + 1;

                if (hour < 19) {
                    if (hour < 16) {
                        if (hour < 11) {
                            if (hour < 8) {
                                result = 0;
                            } else {
                                result = 1;
                            }
                        } else {
                            result = 2;
                        }
                    } else {
                        result = 3;
                    }
                }

                return result;
            },
            location = function () {
                var deferred = $q.defer(),
                    user = User.current();

                $http
                    .get(config.domain + '/map/getMinDistanceStore', {
                        params: {
                            address: ($scope.order.take_address || '').replace(/ /g, '')
                        }
                    })
                    .success(function (result) {
                        if (result && result.flag === 1) {
                            $scope.hiddenTimeRegion = false;
                            $scope.timeRange = checkTimeRange();
                        } else {
                            $scope.hiddenTimeRegion = true;
                        }

                        deferred.resolve();
                    })
                    .catch(function (error) {
                        console.log(error);
                        deferred.resolve();
                    });

                return deferred.promise;
            },
            fetchOrder = function (id) {
                var deferred = $q.defer();

                $http
                    .get(config.domain + '/mobile/orderdetail', {
                        params: {
                            id: id
                        }
                    })
                    .success(function (result) {
                        $scope.order = result;
                        $scope.order.deliverynum = $scope.order.deliverynum || "";
                        $scope.order.paymentValue = $scope.order.paymentValue + '';
                        resume();
                        deferred.resolve();
                    })
                    .catch(function (error) {
                        console.log(error);
                        Loading.tip("应用或服务器异常");
                        deferred.reject(error);
                    });

                return deferred.promise;
            },

            updateProfile = function () {
                var deferred = $q.defer(),
                    user = User.current();

                if (user) {
                    $http
                        .get(config.domain + '/mobile/payinfo', {
                            params: {
                                userid: user.id,
                                price: 0
                            }
                        })
                        .success(function (result) {
                            $scope.balance = user.balance = result.balance;
                            deferred.resolve();
                        })
                        .catch(function (error) {
                            $scope.balance = 0;
                            deferred.resolve();
                        });

                } else {
                    $scope.balance = 0;
                    deferred.resolve();
                }

                return deferred.promise;
            },
            resume = function () {
                var renaminprice = $scope.order.currentprice || 0;

                if ($scope.balanceUsed > 0) {
                    renaminprice -= $scope.balance;
                }

                $scope.renaminprice = renaminprice;

            },
            load = function () {
                $scope.balanceUsed = 0;
                Loading.show();

                fetchOrder(id)
                    .then(location)
                    .then(updateProfile)
                    .then(function () {
                        Loading.close();
                    })
                    .catch(function (error) {
                        Loading.tip('应用异常');
                        $ionicHistory.goBack();
                    });
            };

        $scope.pay = function () {
            if (ionic.Platform.isWebView()) {
                Loading.show(1);

                $http
                    .post(config.domain+'/mobile/pay', $scope.order)
                    .success(function(result) {
                        if (result && result.flag === 2) {
                            AliPay
                                .pay(result.url, {
                                    ono: $scope.order.id
                                })
                                .then(alipayFinishCallback);
                        } else if (result.flag === 1) {
                            Loading.tip('已处理,感谢购买');
                            $ionicHistory.goBack();
                        } else {
                            $ionicHistory.goBack();
                            return Loading.tip(result.msg);
                        }
                    })
                    .catch(function(error) {
                        console.log(error);
                    });

            } else {

                var handler = window.open('http://eofan.com/waiting');
                $http
                    .post(config.domain+'/mobile/pay', $scope.order)
                    .success(function(result) {
                        if (result && result.flag === 2) {
                            handler.location.href=result.url;
                            $ionicPopup.show({
                                title: '请您在新页面上完成付款',
                                template: '<p class="grey">付款完成前请不要关闭此窗口,付款后请点击下面的按钮</p>',
                                scope:$scope,
                                buttons: [
                                    {
                                        text: '已付款',
                                        onTap: function () {
                                            alipayFinishCallback( {
                                                ono: $scope.order.id
                                            });
                                        }
                                    },
                                    {
                                        text: '遇到问题',
                                        type: 'button-assertive',
                                        onTap: function () {
                                            alipayFinishCallback( {
                                                ono: $scope.order.id
                                            });
                                        }
                                    }
                                ]
                            });
                        } else if (result.flag === 1) {
                            Loading.tip('已处理,感谢购买');
                            //$state.go('tab.account');
                            $ionicHistory.goBack();
                        } else {
                            //$state.go('tab.account');
                            $ionicHistory.goBack();
                            return Loading.tip(result.msg);
                        }
                    })
                    .catch(function(error){
                        console.log(error);
                    });
            }
        };
        $scope.useBalance = function () {
            var balance = $scope.balance,
                total = $scope.order.currentprice;

            if (total <= 0) {
                return Loading.tip('当前价格不需要支付');
            }

            if (balance <= 0) {
                return Loading.tip('您的余额不足, 请充值');
            }

            $state.go('tab.continue-pay-balance', {
                total: total,
                balance: balance
            });
        };
        $scope.$root.$on('pay-balance', function (event, args) {
            $scope.balanceUsed = parseFloat($filter('number')(args.use, 2));
            $scope.payUseBalance = true;
            resume();
        });
        $scope.$root.$on('cancel-balance', function (event, args) {
            $scope.balanceUsed = 0;
            $scope.payUseBalance = false;
            resume();
        });

        load();
    })
    /*订单详情control*/
    .controller('OrderDetailCtrl', function ($scope, $state, $resource, $http, $ionicPopup, $ionicHistory, AliPay, MyOrders, Loading) {
        var id = $state.params.id,
            fetchOrder = function (id) {
                Loading.show();
                orderHelper.get({
                        id: id
                    },
                    function (data) {
                        Loading.close();
                        $scope.order = data;
                        $scope.$root.$broadcast('order:fetchSuccess', {
                            order: data
                        });

                        fetchExpress(data.deliverynum);
                    },
                    function (data) {
                        Loading.tip('应用异常');
                        console.log(data);
                    });
            },
            fetchExpress = function (devilyNumber) {
                $http.get('http://www.kuaidi100.com/query?type=zhaijisong&postid=' + devilyNumber)
                    .success(function (result) {
                        if (result && result.status == '200') {
                            return $scope.expresses = result.data;
                        }

                        $scope.expressProgress = '正在处理';
                        console.log(result);
                    })
                    .error(function (result) {
                        $scope.expressProgress = '查询异常,请稍后再试';
                    });
            },
            orderHelper = $resource(config.domain + '/mobile/orderdetail'),
            alipayFinishCallback = function (args) {
                Loading.show(1);
                $http
                    .get(config.domain + '/mobile/order/status?orderid=' + args.ono)
                    .success(function (result) {
                        if (result) {
                            if (result.flag == 1) {
                                Loading.tip('您已支付成功');
                            } else {
                                Loading.tip('没有支付成功');
                            }
                        } else {
                            Loading.tip('支付存在问题, 请到 我的订单 中确认');
                        }

                        $ionicHistory.goBack();
                    })
                    .catch(function (error) {
                        Loading.tip('网络或服务器出现错误');
                        $ionicHistory.goBack();
                    });
            };


        $scope.expressProgress = '正在查询, 请稍后';
        $scope.status = status;
        $scope.paying = false;
        $scope.continuePay = function () {
            $state.go('tab.continue-pay', {
                id: id
            });
            return;
            if ($scope.paying) {
                return;
            }

            $scope.paying = false;
            Loading.show(1);
            var resource = $resource(config.domain + '/mobile/pay');
            resource.save($scope.order,
                function (result) {
                    if (result && result.flag === 2) {
                        AliPay.pay(result.url, {
                            ono: $scope.order.id
                        })
                            .then(alipayFinishCallback);
                    } else {
                        Loading.tip(result.msg);
                        $scope.paying = false;
                    }
                },
                function (error) {
                    Loading.tip('支付失败，请稍后再试');
                    console.log(error);
                    $scope.paying = false;
                }
            );
        };
        $scope.cancelOrder = function () {
            var resource = $resource(config.domain + '/mobile/user/order/changestatus');
            if ($scope.order.status !== '待付款' && ($scope.order.paymentValue == '1' || $scope.order.paymentValue == '3')) {

                $ionicPopup.show({
                    title: '退款说明',
                    template: '<p class="grey">账户余额可立即到账, 原路返回支付宝需要5-7个工作日</p>',
                    buttons: [
                        {
                            text: '原路返回',
                            onTap: function () {
                                Loading.show();
                                resource = $resource(config.domain + '/mobile/user/order/changestatus');
                                resource.save({
                                    status: 5,
                                    id: $state.params.id,
                                    refund: 0
                                }, function (result) {
                                    if (result.err == 1) {
                                        return Loading.tip(result.msg);
                                    }

                                    Loading.close();
                                    $scope.$root.$broadcast('cancelOrder', {
                                        id: $state.params.id
                                    });
                                    $ionicHistory.goBack();
                                }, function (error) {
                                    Loading.tip('应用异常');
                                    console.log(error);
                                });
                            }
                        },
                        {
                            text: '账户余额',
                            type: 'button-assertive',
                            onTap: function () {
                                Loading.show();
                                resource = $resource(config.domain + '/mobile/user/order/changestatus');
                                resource.save({
                                    status: 5,
                                    id: $state.params.id,
                                    refund: 1
                                }, function (result) {
                                    if (result.err == 1) {
                                        return Loading.tip(result.msg);
                                    }

                                    Loading.close();
                                    $scope.$root.$broadcast('cancelOrder', {
                                        id: $state.params.id
                                    });
                                    $ionicHistory.goBack();
                                }, function (error) {
                                    Loading.tip('应用异常');
                                    console.log(error);
                                });
                            }
                        },
                        {
                            text: '取消'
                        }
                    ]
                });
            } else {
                Loading.show();

                resource = $resource(config.domain + '/mobile/user/order/changestatus');
                resource.save({
                    status: 5,
                    id: $state.params.id,
                    refund: 0
                }, function (result) {
                    if (result.err == 1) {
                        return Loading.tip(result.msg);
                    }

                    Loading.close();
                    $scope.$root.$broadcast('cancelOrder', {
                        id: $state.params.id
                    });
                    $ionicHistory.goBack();
                }, function (error) {
                    Loading.tip('应用异常');
                    console.log(error);
                });
            }
        };
        $scope.comment = function (oiid, psid) {
            $state.go('tab.order-comment', {
                oiid: oiid,
                psid: psid
            });
        };
        $scope.$root.$on('comment', function (event, args) {
            var comment = args.comment;

            $scope.order.items = _.map($scope.order.items, function (item) {
                if (item.id == comment.oiid) {
                    item.hascomment = 1;
                }

                return item;
            });
        });
        $scope.$on('$ionicView.afterEnter', function () {
            fetchOrder(id);
        });

    })
    .controller('InviteCtrl', function ($scope, $base64, User, Loading) {
        var user = User.current(),
            title = '我发现了一个很方便的果蔬速递网站，质量价格都不错，来试试吧！',
            url = 'http://www.eofan.com/signup?c=' + $base64.encode(user.mobile);

        $scope.share = function () {
            if (window.plugins && window.plugins.socialsharing) {
                window.plugins.socialsharing.share(title + ' ' + url);
            }
        };
        $scope.copy = function () {
            Loading.tip('已复制');
        };
        $scope.content = title + ' ' + url;
    })
    /*购物车Control*/
    .controller('CarCtrl', function ($scope, $resource, $filter, $state, $ionicPopup, $http, User, ShopCar, Loading) {
        var refresh = function () {
                var all = ShopCar.all();
                $scope.all = all;
                $scope.gifts = [];
                $scope.cars = _.filter(all, function (cart) {
                    return (!cart.type) || ( cart.type && cart.type !== 2);
                });
                $scope.presales = _.filter(all, function (cart) {
                    return cart.type && cart.type === 2;
                });
                $scope.gifts = ShopCar.getGifts() || [];
            },
            resume = function () {
                var total = 0;

                _.each(_.where($scope.cars, {
                    checked: true
                }), function (record) {
                    var t = $filter('number')((record.quantity * record.product.price), 2);
                    total += parseFloat(t);
                });

                _.each(_.where($scope.presales, {
                    checked: true
                }), function (record) {
                    var t = $filter('number')((record.quantity * record.product.price), 2);
                    total += parseFloat(t);
                });

                $scope.total = $filter('number')(total, 2);
                $scope.showPresaleWarning = ($scope.cars.length > 0 && $scope.presales.length > 0) || ($scope.gifts.length > 0 && $scope.presales.length > 0);
            };

        $scope.gifts = [];
        $scope.cars = [];
        $scope.presales = [];
        $scope.config = config;
        $scope._ = _;

        $scope.$root.$on('removeCar', function () {
            refresh();
        });
        $scope.$watch('cars', function () {
            resume();
        }, true);
        $scope.$watch('presales', function () {
            resume();
        }, true);
        $scope.removeCopie = function (pid, psid, poid) {
            $ionicPopup.show({
                title: '询问',
                template: '是否要从购物车移除?',
                buttons: [
                    {
                        text: '<b >是</b>',
                        type: 'button-balanced',
                        onTap: function () {
                            var userId = null;
                            if (User.current()) {
                                userId = User.current().id;
                            }

                            $http
                                .post(config.domain + '/mobile/remove_offline_car', {
                                    userid: userId,
                                    items: _.where($scope.cars, {
                                        pid: pid,
                                        psid: psid,
                                        poid: poid
                                    })
                                })
                                .success(function () {
                                    ShopCar.removeOffline(userId, {
                                        pid: pid,
                                        psid: psid,
                                        poid: poid
                                    });
                                    $scope.cars = ShopCar.all();
                                })
                                .catch(function (error) {
                                    console.log(error);
                                });
                        }
                    },
                    {
                        text: '否'
                    }
                ]
            });
        };
        $scope.showPresaleDetail = function (id) {
            var exist = _.find($scope.presales, function (item) {
                return (item.psid === parseInt(id));
            });

            if (exist) {
                ShopCar.setPresaleForDetail(exist.product);
                $state.go('tab.pre-sale-detail');
            }
        };
        $scope.addQuantity = function (pid, psid, num) {
            var record = _.where($scope.all, {
                    pid: pid,
                    psid: psid
                }),
                resource = $resource(config.domain + '/mobile/check_cart'),
                user = User.current();

            if (record.length > 0) {
                record = record[0];
            }
            if (record) {
                var quantity = record.quantity + num;
                if (quantity < 1) {
                    quantity = 1;
                }

                if (record.renaming && record.renaming > 0 && quantity > record.renaming) {
                    return Loading.tip('抱歉，库存不足');
                }

                if (record.limit && record.limit > 0 && quantity > record.limit) {
                    return Loading.tip('抱歉，当前商品最多可购买' + record.limit + '份');
                }

                if (user) {
                    Loading.show();
                    resource.get({
                        uid: user.id,
                        psid: record.psid,
                        pid: record.pid,
                        quantity: quantity
                    }, function (result) {
                        if (result && result.flag === 1) {
                            record.quantity = quantity;
                            return Loading.close();
                        }

                        if (result.count < 0) {
                            result.count = 0;
                        }
                        record.quantity = result.count;
                        Loading.tip(result.msg);
                    }, function (error) {
                        Loading.close();
                    });
                } else {
                    record.quantity = quantity;
                }
            }

        };
        $scope.pay = function (pid, psid) {
            var payOptionals = [],
                giftsToUse = _.where($scope.gifts, {
                    checked: true
                });

            _.each($scope.cars, function (cart) {
                if (cart.checked) {
                    payOptionals.push(cart);
                }
            });

            _.each($scope.presales, function (cart) {
                if (cart.checked) {
                    payOptionals.push(cart);
                }
            });

            ShopCar.setPayOptionals(payOptionals);
            ShopCar.setUseGifts(giftsToUse);

            $state.go('tab.pay', {}, {
                reload: true
            });
        };
        $scope.checkAll = function () {
            _.each($scope.cars, function (car) {
                if (car && car.product && car.product.status == '1') {
                    car.checked = true;
                }
            });

            _.each($scope.gifts, function (gift) {
                gift.checked = true;
            });
        };
        $scope.removeCar = function (pid, psid) {
            $ionicPopup.show({
                title: '询问',
                template: '是否要从购物车移除?',
                buttons: [
                    {
                        text: '<b >是</b>',
                        type: 'button-balanced',
                        onTap: function () {
                            var userId = null;
                            if (User.current()) {
                                userId = User.current().id;
                            }

                            ShopCar.remove(userId, {
                                pid: pid,
                                psid: psid
                            });
                            refresh();
                        }
                    },
                    {
                        text: '否'
                    }
                ]
            });
        };
        $scope.showOfflineDetail = function (psid, storeID) {
            $state.go('tab.cart-store-categories-product', {
                id: psid,
                storeID: storeID
            });
        };
        $scope.showDetail = function (pid) {
            $state.go('tab.car-product', {
                id: pid
            });
        };
        $scope.$on('$ionicView.afterEnter', function () {
            Loading.show();
            User.updateProfile();
        });
        $scope.$on('user:updateProfileSuccess', function () {
            Loading.close();
            refresh();
        });
    })
    /*
     *支付Control
     */
    .controller('PaymentCtrl', function ($scope, $state, $filter, $resource, $timeout, $ionicHistory,$ionicPopup, $ionicScrollDelegate, AliPay, $http, $q, ShopCar, MyAddress, User, Loading) {
        var order = {},
            extra = $state.params.extra || 'NORMAL',
            items = [],
            presales = [],
            freeShippingFee = 0,
            shippingFee = 0,
            discountThreshold = 0,
            discount = 0,
            user = User.current(),
            cars = [],
            gifts = [],
            profileWithoutAddress = function () {
                var resource = $resource(config.domain + '/mobile/payinfo'),
                    deferred = $q.defer();

                resource.get({
                        userid: user.id,
                        price: order.currentprice
                    },
                    function (result) {
                        user.addresses = result.address;
                        user.balance = result.balance;
                        discountThreshold = parseFloat($filter('number')(result.discountthreshold, 2)) || 0;
                        discount = parseFloat($filter('number')(result.discount, 2)) || 0;
                        freeShippingFee = parseFloat($filter('number')(result.freeshippingfee, 2));
                        shippingFee = parseFloat($filter('number')(result.shippingfee, 2));
                        $scope.freeShippingFee = freeShippingFee;
                        deferred.resolve();
                    },
                    function (error) {
                        console.log(error);
                        deferred.reject('应用异常，没有获取到支付信息');
                    });

                return deferred.promise;
            },
            profile = function () {
                var resource = $resource(config.domain + '/mobile/payinfo'),
                    deferred = $q.defer();

                resource.get({
                        userid: user.id,
                        price: order.currentprice
                    },
                    function (result) {
                        user.addresses = result.address;
                        user.balance = result.balance;
                        discountThreshold = parseFloat($filter('number')(result.discountthreshold, 2)) || 0;
                        discount = parseFloat($filter('number')(result.discount, 2)) || 0;
                        freeShippingFee = parseFloat($filter('number')(result.freeshippingfee, 2));
                        shippingFee = parseFloat($filter('number')(result.shippingfee, 2));
                        $scope.freeShippingFee = freeShippingFee;
                        defaultAddress = MyAddress.getDefaultAddress(user.addresses);
                        if (defaultAddress) {
                            order.addrid = 0 || defaultAddress.id;
                        }
                        deferred.resolve();
                    },
                    function (error) {
                        console.log(error);
                        deferred.reject('应用异常，没有获取到支付信息');
                    });

                return deferred.promise;
            },
            checkProducts = function () {
                var deferred = $q.defer();

                order.payment = '1';
                order.coupon_code = '';
                order.balance = 0;
                order.coupon = 0;

                items = [];
                presales = [];
                cars = [];
                gifts = [];

                if (extra == 'NORMAL') {
                    cars = ShopCar.getPayOptionals();
                    _.each(cars, function (car) {
                        items.push({
                            type: car.type,
                            poid: car.poid,
                            psid: car.psid,
                            quantity: car.quantity,
                            price: car.product.price,
                            storeid: car.product.storeid,
                            name: car.product.name,
                            cover: config.domain + '/upload/' + car.product.sku + '/' + car.product.cover
                        });
                    });

                    gifts = ShopCar.getUseGifts();
                    order.items = items;
                    order.giftitems = gifts;

                    if (cars.length === 0 && gifts.length === 0) {
                        deferred.reject('emptyProducts');
                    } else {
                        deferred.resolve();
                    }
                }

                if (extra == 'PRESALE') {
                    presales = ShopCar.getPresales();

                    if (presales.length === 0) {
                        deferred.reject('emptyProducts');
                    } else {
                        deferred.resolve();
                    }
                }


                return deferred.promise;
            },
            coupons = function () {
                var resource = $resource(config.domain + '/mobile/coupons'),
                    deferred = $q.defer(),
                    total = order.currentprice;

                if (extra === 'PRESALE') {
                    deferred.resolve();
                } else {
                    resource.query({
                        userid: User.current().id,
                        type: 'unuse'
                    }, function (result) {
                        var coupons = _(result)
                            .chain()
                            .reject(function (coupon) {
                                return total <= coupon.minprice || total <= coupon.price;
                            })
                            .sortBy('endtime')
                            .reverse()
                            .sortBy('price')
                            .reverse()
                            .value();

                        coupon = coupons[0];

                        if (coupons.length > 0) {
                            $scope.$root.$broadcast('pay-coupon', {
                                amount: parseFloat(coupon.price),
                                coupon: coupon
                            });
                        }

                        deferred.resolve();
                    }, function (err) {
                        console.log(err);
                        deferred.reject('应用异常, 没有自动使用优惠券');
                    });
                }

                return deferred.promise;
            },
            location = function () {
                var deferred = $q.defer(),
                    defaultAddress = null,
                    user = User.current();

                if (!user) {
                    deferred.resolve();
                }

                var presales = _.filter(items, function (item) {
                    return item.type === 2;
                });

                if (presales.length > 0) {
                    $scope.hiddenDayRegion = true;
                    $scope.hiddenTimeRegion = true;
                    $scope.hiddenStoreProducts = true;
                    deferred.resolve();
                } else {
                    defaultAddress = MyAddress.getAddressByID(order.addrid, user.addresses);
                    $http
                        .get(config.domain + '/map/getMinDistanceStore', {
                            params: {
                                address: defaultAddress.province + defaultAddress.city + defaultAddress.region + defaultAddress.street + defaultAddress.address
                            }
                        })
                        .success(function (result) {
                            if (result && result.flag === 1) {
                                order.storeid = result.data.id;
                                $scope.storeProducts = [];
                                var productsInStore = _.filter(items, function (item) {
                                    return item.storeid && item.storeid !== order.storeid;
                                });

                                if (productsInStore.length > 0) {
                                    $scope.hiddenNextStep = true;
                                    $scope.hiddenDayRegion = true;
                                    $scope.hiddenTimeRegion = true;
                                    $scope.hiddenPaymentRegion = true;
                                    $scope.hiddenFeeRegion = true;
                                    $scope.hiddenStoreProducts = false;
                                    $scope.storeProducts = productsInStore;
                                    return deferred.reject('shouldNotStoreProduct');
                                }


                                $scope.freeShippingFee = freeShippingFee = parseFloat($filter('number')(result.data.byprice || 0, 2));
                                $scope.shippingFee = shippingFee = parseFloat($filter('number')(result.data.freight || 0, 2));
                                $scope.hiddenDayRegion = true;
                                $scope.hiddenTimeRegion = false;
                                $scope.hiddenPaymentRegion = false;
                                $scope.hiddenFeeRegion = false;
                                $scope.hiddenStoreProducts = true;
                                $scope.hiddenNextStep = false;
                                $scope.timeRange = checkTimeRange();
                                if ($scope.timeRange === 4) {
                                    order.delivery_day = 'morning';
                                } else {
                                    switch ($scope.timeRange) {
                                        case 0:
                                        case 1:
                                            order.delivery_day = 'morning';
                                            break;

                                        case 2:
                                            order.delivery_day = 'noon';
                                            break;

                                        case 3:
                                            order.delivery_day = 'afternoon';
                                            break;
                                    }
                                }

                                deferred.resolve();
                            } else {

                                $scope.storeProducts = [];
                                var productsInStore = _.filter(items, function (item) {
                                    return item.storeid > 0;
                                });

                                if (productsInStore.length > 0) {
                                    $scope.hiddenNextStep = true;
                                    $scope.hiddenDayRegion = true;
                                    $scope.hiddenTimeRegion = true;
                                    $scope.hiddenPaymentRegion = true;
                                    $scope.hiddenFeeRegion = true;
                                    $scope.hiddenStoreProducts = false;
                                    $scope.storeProducts = productsInStore;
                                    return deferred.reject('shouldNotStoreProduct');
                                } else {
                                    $scope.hiddenNextStep = false;
                                    $scope.hiddenDayRegion = false;
                                    $scope.hiddenTimeRegion = false;
                                    $scope.hiddenPaymentRegion = false;
                                    $scope.hiddenFeeRegion = false;
                                    $scope.hiddenTimeRegion = true;
                                    $scope.hiddenStoreProducts = true;
                                    deferred.resolve();
                                }
                            }

                        })
                        .catch(function (error) {
                            console.log(error);
                            $scope.store = false;
                            deferred.reject('locationException');
                        });
                }

                return deferred.promise;
            },
            checkTimeRange = function () {
                var now = new Date(),
                    result = 4,
                    hour = now.getHours() + 1;

                if (hour < 19) {
                    if (hour < 16) {
                        if (hour < 11) {
                            if (hour < 8) {
                                result = 0;
                            } else {
                                result = 1;
                            }
                        } else {
                            result = 2;
                        }
                    } else {
                        result = 3;
                    }
                }

                return result;
            },
            load = function (total) {
                Loading.show();

                checkProducts()
                    .then(profile)
                    .then(location)
                    .then(resume)
                    .then(coupons)
                    .then(resume)
                    .then(function () {
                        Loading.close();
                        $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
                    })
                    .catch(function (error) {

                        Loading.close();
                        var via = error || '';

                        if (via === 'emptyProducts') {
                            Loading.tip('没有要支付的商品');
                            return $ionicHistory.goBack();
                        }

                        $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
                    });
            },
            resume = function () {
                var price = 0,
                    deferred = $q.defer();

                // 计算总价格
                // price = 商品价格
                // currentprice = 商品价格 + 邮费 - 优惠卷
                // shippingprice = 邮费
                $scope.order.price = 0;
                $scope.order.shippingprice = 0;
                $scope.differenceWithShipping = 0;
                $scope.order.offPrice = 0;
                $scope.offs = [];
                _.each(cars, function (car) {
                    price = $filter('number')((car.quantity * car.product.price), 2);
                    $scope.order.price += parseFloat(price);
                });
                _.each(presales, function (presaleItem) {
                    price = $filter('number')((presaleItem.quantity * presaleItem.price), 2);
                    $scope.order.price += parseFloat(price);
                });
                //$scope.order.price += order.shippingprice;
                $scope.order.price = parseFloat($filter('number')($scope.order.price, 2));

                if ($scope.order.price < freeShippingFee) {
                    $scope.differenceWithShipping = parseFloat($filter('number')(freeShippingFee - $scope.order.price, 2));
                    $scope.order.shippingprice = shippingFee;
                    $scope.order.currentprice += shippingFee;
                }

                // 计算应支付的金额
                // 应支付的金额 ＝ 商品价格 ＋ 物流费用 － 优惠券
                $scope.order.currentprice = 0;
                $scope.order.currentprice = parseFloat($filter('number')($scope.order.price - $scope.order.coupon + $scope.order.shippingprice, 2));
                if ($scope.order.currentprice >= discountThreshold) {
                    $scope.order.currentprice -= discount;
                    $scope.order.offPrice = discount;

                    if (discountThreshold != discount != 0) {
                        $scope.offs.push('全场满' + discountThreshold + '元减' + discount + '元');
                    }
                }

                // 还需支付的金额
                // 还需支付的金额 = 商品价格 ＋ 物流费用 － 优惠券 － 余额
                $scope.renaminprice = parseFloat($filter('number')($scope.order.price - $scope.order.coupon - $scope.order.balance - $scope.order.offPrice + $scope.order.shippingprice, 2));
                deferred.resolve();
                return deferred.promise;
            },
            alipayFinishCallback = function (args) {
                Loading.show(1);
                $http
                    .get(config.domain + '/mobile/order/status?orderid=' + args.orderid)
                    .success(function (result) {
                        if (result) {
                            if (result.flag == 1) {
                                Loading.tip('订单已提交, 感谢购买');
                            } else {
                                Loading.tip('订单已提交, 请及时支付');
                            }
                        } else {
                            Loading.tip('订单没有正确提交, 请到 我的订单 中确认');
                        }

                        $ionicHistory.goBack();
                    })
                    .catch(function (error) {
                        Loading.tip('网络或服务器出现错误');
                        $ionicHistory.goBack();
                    });
            };

        //price 商品价格
        order.price = 0;
        order.currentprice = 0;
        order.shippingprice = 0;
        order.offPrice = 0;
        order.delivery_day = '';
        order.items = items;
        order.giftitems = gifts;
        order.msitems = [];
        order.yitems = presales;
        order.payment = '1';
        order.coupon_code = '';
        order.balance = 0;
        order.coupon = 0;
        order.userid = user.id;
        order.msg = '';

        $scope.expandAddress = function () {
            $scope.showAllAddress = true;
        };
        $scope.collapseAddress = function () {
            $scope.showAllAddress = false;
            var user = User.current();
            _.each(user.addresses, function (address, index) {
                if (address.id == user.defaultAddressID) {
                    user.addresses.splice(0, 0, user.addresses.splice(index, 1)[0]);
                }
            });
        };
        $scope.pay = function () {
            if (!$scope.order.addrid || $scope.order.addrid === 0) {
                return Loading.tip('请选择收货地址');
            }

            if ($scope.paying) {
                return;
            }
            $scope.paying = true;

            //0货到付款  1支付宝  2账户余额 3网银支付 4 余额合并 5 收货地址合并
            if ($scope.payUseBalance) {
                //使用余额支付
                if ($scope.renaminprice > 0) {
                    //使用余额支付一部分
                    if ($scope.source.payment == '0') {
                        //其余部分货到付款时
                        order.payment = '5';
                    } else {
                        //其余部分使用支付宝
                        order.payment = '4';
                    }
                } else {
                    //使用余额支付了全部
                    order.payment = '2';
                }
            } else {
                order.payment = $scope.source.payment;
            }

            var resource = $resource(config.domain + '/mobile/pay');

            if (ionic.Platform.isWebView()) {
                Loading.show(1);

                $http
                    .post(config.domain+'/mobile/pay', order)
                    .success(function(result) {
                        if (result && result.flag === 2) {
                            AliPay
                                .pay(result.url, result)
                                .then(alipayFinishCallback);
                        } else if (result.flag === 1) {
                            Loading.tip('订单下单成功,感谢购买')
                            $ionicHistory.goBack();
                        } else {
                            $ionicHistory.goBack();
                            return Loading.tip(result.msg);
                        }
                    })
                    .catch(function(error) {
                        console.log(error);
                    });

            } else {
                var handler = window.open('http://eofan.com/waiting');
                $http
                    .post(config.domain+'/mobile/pay', order)
                    .success(function(result) {
                        if (result && result.flag === 2) {
                            handler.location.href=result.url;
                            $ionicPopup.show({
                                title: '请您在新页面上完成付款',
                                template: '<p class="grey">付款完成前请不要关闭此窗口,付款后请点击下面的按钮</p>',
                                scope:$scope,
                                buttons: [
                                    {
                                        text: '已付款',
                                        onTap: function () {
                                            alipayFinishCallback(result);
                                        }
                                    },
                                    {
                                        text: '遇到问题',
                                        type: 'button-assertive',
                                        onTap: function () {
                                            alipayFinishCallback(result);
                                        }
                                    }
                                ]
                            });
                        } else if (result.flag === 1) {
                            Loading.tip('订单下单成功,感谢购买');
                            //$state.go('tab.account');
                            $ionicHistory.goBack();
                        } else {
                            //$state.go('tab.account');
                            $ionicHistory.goBack();
                            return Loading.tip(result.msg);
                        }
                    })
                    .catch(function(error){
                        console.log(error);
                    });
            }
        };
        $scope.setAddress = function (id) {
            Loading.show();
            $scope.order.addrid = id;
            $scope.showAllAddress = false;

            profileWithoutAddress()
                .then(location)
                .then(resume)
                .then(coupons)
                .then(resume)
                .then(function () {
                    Loading.close();
                    $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
                })
                .catch(function (error) {
                    Loading.close();
                    var via = error || '';

                    if (via === 'emptyProducts') {
                        Loading.tip('没有要支付的商品');
                        return $ionicHistory.goBack();
                    }

                    $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
                });
        };
        $scope.modifyAddress = function (id) {
            $scope.$root.new = false;
            $scope.$root.address = MyAddress.getAddressByID(id, User.current().addresses);
            $state.go($state.$current.name + '-address-edit', {
                id: id
            });
        };
        $scope.newAddress = function (id) {
            $scope.$root.new = true;
            $scope.$root.address = {
                province: '陕西省',
                city: '西安市',
                userid: User.current().id,
                tel: '',
                mobile: ''
            };
            $state.go($state.$current.name + '-address-edit', {
                id: id
            });
        };
        $scope.useBalance = function () {
            var balance = User.current().balance || 0,
                total = $scope.order.currentprice;

            if (total <= 0) {
                return Loading.tip('当前价格不需要支付');
            }

            if (balance <= 0) {
                return Loading.tip('您的余额不足, 请充值');
            }

            $state.go($state.$current.name + '-balance', {
                total: total,
                balance: balance
            });
        };
        $scope.useCoupon = function () {
            var balance = $scope.order.balance,
                total = parseFloat($scope.order.price - balance);

            if (total < 0) {
                total = 0;
            }

            $state.go('tab.pay-coupon', {
                total: total
            });
        };
        $scope.showOffPriceDetail = function () {
            $scope.isShowOffPriceDetail = !$scope.isShowOffPriceDetail;
        };
        $scope.removeStoreProduct = function () {
            var productsInStore = $scope.storeProducts || [],
                cars = ShopCar.getPayOptionals(),
                user = User.current();

            _.each(productsInStore, function (product) {
                cars = _.reject(cars, function (item) {
                    return item.psid === product.psid;
                });
            });

            ShopCar.setPayOptionals(cars);
            load();
        };

        $scope.$root.$on('address:saveNewSuccess', function (event, args) {
            if (args.address) {
                $scope.setAddress(args.address.id);
            }
        });
        $scope.$root.$on('pay-balance', function (event, data) {
            $scope.order.balance = parseFloat($filter('number')(data.use, 2));
            $scope.payUseBalance = true;
            resume();
        });
        $scope.$root.$on('cancel-balance', function (event, data) {
            $scope.order.balance = 0;
            $scope.payUseBalance = false;
            resume();
        });
        $scope.$root.$on('pay-coupon', function (event, data) {
            $scope.order.coupon = parseFloat($filter('number')(data.amount, 2));
            $scope.order.coupon_code = data.coupon.code;
            $scope.payUseCoupon = true;
            resume();
        });
        $scope.$root.$on('cancel-coupon', function (event, data) {
            $scope.order.coupon = 0;
            $scope.order.coupon_code = '';
            $scope.payUseCoupon = false;
            resume();

        });
        $scope.extra = extra;
        $scope.paying = false;
        $scope.parseFloat = parseFloat;
        $scope.showAllAddress = false;
        $scope.order = order;
        $scope.user = user;
        $scope.payType = '1';
        $scope.source = {
            payment: '1'
        };
        $scope.offs = [];
        $scope.isShowOffPriceDetail = false;

        load($scope.order.price);
    })
    /*
     使用优惠券路由
     */
    .controller('CouponPayCtrl', function ($scope, $state, $window, $resource, $ionicScrollDelegate, $ionicHistory, User, Loading) {
        var total = parseFloat($state.params.total),
            query = function (type) {
                var resource = $resource(config.domain + '/mobile/coupons');
                Loading.show();
                resource.query({
                    userid: User.current().id,
                    type: type
                }, function (result) {
                    $scope.coupons = [];

                    _.each(result, function (coupon) {
                        if (total >= coupon.minprice && total >= coupon.price) {
                            $scope.coupons.push(coupon);
                        }
                    });
                    $ionicScrollDelegate.resize();
                    Loading.close();
                }, function (err) {
                    console.log(err);
                    Loading.tip('应用异常');
                });
            };

        $scope.total = total;
        $scope.pay = function (code) {
            var exists = _.where($scope.coupons, {
                code: code
            });
            if (exists.length === 0) {
                return Loading.tip('选择失败请重试');
            }

            var use = exists[0];
            if (use.price > total) {
                return Loading.tip('支付券金额不能大于商品金额');
            }

            $scope.$root.$broadcast('pay-coupon', {
                total: total,
                coupon: use,
                amount: use.price
            });
            $ionicHistory.goBack();
        };
        $scope.cancel = function () {
            Loading.tip('已取消使用优惠券支付');
            $scope.$root.$broadcast('cancel-coupon');
            $ionicHistory.goBack();
        };

        query('unuse');
    })
    /*
     使用余额路由
     */
    .controller('BalanceCtrl', function ($scope, $state, $filter, $window, $ionicHistory, $timeout, User, Loading) {
        var total = parseFloat($filter('number')($state.params.total, 2)),
            balance = parseFloat($filter('number')($state.params.balance, 2));

        $scope.total = total;
        $scope.balance = balance;
        $scope.use = balance > total ? total : balance;
        $scope.value = $scope.use;
        $scope.$watch('value', function (value, old) {
            var value = $filter('number')(value, 2);

            if (value !== old && value <= $scope.balance) {
                $scope.use = value > total ? total : value;
            }
        });
        $scope.pay = function () {
            $scope.$root.$broadcast('pay-balance', {
                use: $scope.use,
                total: $scope.total
            });
            $ionicHistory.goBack();
        };
        $scope.cancel = function () {
            $scope.$root.$broadcast('cancel-balance');
            Loading.tip('已取消使用余额支付');
            $ionicHistory.goBack();
        };

    })
    /*
     我的优惠券路由
     */
    .controller('CouponsCtrl', function ($scope, $state, $window, $ionicScrollDelegate, $resource, User, Loading) {
        var query = function (type) {
            var resource = $resource(config.domain + '/mobile/coupons');
            Loading.show();
            resource.query({
                userid: User.current().id,
                type: type
            }, function (result) {
                $scope.coupons = result;
                $ionicScrollDelegate.resize();
                Loading.close();
            }, function (err) {
                console.log(err);
                Loading.tip('应用异常');
            });
        };

        $scope.switch = function (type) {
            $ionicScrollDelegate.scrollTop();
            $scope.choose = type;
            query(type);
        };

        $scope.switch('unuse');
    })
    /*我的收藏Control*/
    .controller('FavoriteCtrl', function ($scope, $state, $resource, $ionicPopup, $ionicLoading, User, Favorite, Loading) {
        Loading.show()
        var favoriteHelper = $resource(config.domain + '/mobile/favorite');
        favoriteHelper.query({
                userid: User.current().id
            },
            function (data) {
                Loading.close();
                $scope.items = _.map(data, function (item) {
                    item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                    return item;
                });
                Favorite.mine = $scope.items;
                Favorite.scope = $scope;
            },
            function (data) {
                Loading.tip('应用异常');
            });
        $scope.showDetail = function (id) {
            $state.go($state.$current.name + '-product', {
                id: id
            });
        };
        $scope.remove = function (id) {
            var userId = null;
            if (User.current()) {
                userId = User.current().id;
            }

            Favorite.remove(userId, id);
            $scope.items = _.reject($scope.items, function (item) {
                return item.id == id;
            });
        };
    })
    /*账户余额control*/
    .controller('CostCtrl', function ($scope, $state, $timeout, $resource, $http, $ionicHistory, $ionicScrollDelegate, AliPay, User, Loading) {
        var costHelper = $resource(config.domain + '/mobile/balance'),
            alipayFinishCallback = function (args) {
                Loading.show(1);
                $http
                    .get(config.domain + '/mobile/cost/status?userid=' + args.userID + '&price=' + args.price + '&maxid=' + args.maxID)
                    .success(function (result) {
                        if (result) {
                            if (result.flag == 1) {
                                Loading.tip('充值成功');
                            } else {
                                Loading.tip('充值没有成功');
                            }
                        } else {
                            Loading.tip('充值存在问题');
                        }

                        $ionicHistory.goBack();
                    })
                    .catch(function (error) {
                        Loading.tip('网络或服务器出现错误');
                        $ionicHistory.goBack();
                    });
            };

        $scope.paying = false;
        $scope.$root.czprice = 0;
        $scope.minID = 9999999999;

        $scope.fetch = function () {
            costHelper.get({
                    userid: User.current().id,
                    minid: $scope.minID
                },
                function (data) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    if (data && data.items) {
                        if (data.items.length > 0) {
                            $scope.minID = data.items[data.items.length - 1].id;
                            $scope.hasMore = true;

                            switch ($scope.choose) {
                                case 'IN':
                                    $scope.hasMore = _.where(data.items, {
                                        stype: '收入'
                                    }).length > 0;
                                    break;

                                case 'OUT':
                                    $scope.hasMore = _.where(data.items, {
                                        stype: '支出'
                                    }).length > 0;
                                    break;
                            }

                        } else {
                            $scope.hasMore = false;
                        }

                        $scope.balances = _.union($scope.balances, data.items);
                        $scope.balance = data.balance;

                        if ($scope.balance.length > 0) {
                            $scope.$root.balanceMaxID = $scope.balances[0].id;
                        }

                        $ionicScrollDelegate.resize();
                    }

                    Loading.close();

                },
                function (data) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    console.log(data);
                    Loading.tip('网络异常');
                });
        };
        $scope.switch = function (type) {
            $scope.hasMore = true;
            $scope.choose = type;
            $ionicScrollDelegate.resize();

        };
        $scope.paying = false;
        $scope.chongzhi = function () {
            $scope.paying = false;

            Loading.show(1);
            var resource = $resource(config.domain + '/mobile/alipay_cz');
            resource.save({
                    price: $scope.$root.czprice,
                    userid: User.current().id
                },
                function (result) {
                    if (result && result.flag === 1) {
                        var maxID = $scope.$root.balanceMaxID || 0;

                        AliPay.pay(result.url, {
                            userID: User.current().id,
                            price: $scope.$root.czprice,
                            maxID: maxID
                        })
                            .then(alipayFinishCallback);
                    } else {
                        $scope.paying = false;
                        Loading.tip(result.msg);
                    }
                },
                function (result) {
                    Loading.tip('提交订单失败');
                    $scope.paying = false;
                    console.log(result);
                }
            );
        };

        $scope.choose = 'ALL';
        $scope.balance = 0;
        $scope.$on('$ionicView.afterEnter', function () {
            $scope.$apply(function () {
                $scope.balances = [];
                $scope.minID = 9999999999;
                $scope.hasMore = true;
                $ionicScrollDelegate.scrollTop();
            })

        });
    })
    /*地址管理control*/
    .controller('AddressCtrl', function ($scope, $state, $resource, $rootScope, $ionicHistory, MyAddress, $window, User, Loading) {
        var user = User.current(),
            resource = $resource(config.domain + '/mobile/address'),
            fetch = function () {
                Loading.show();

                resource.query({
                        userid: user.id
                    },
                    function (data) {
                        Loading.close();
                        user.addresses = data;
                    },
                    function (err) {
                        console.log(err);
                        Loading.tip('应用异常');
                    });
            };

        $scope.newAddress = function () {
            $scope.$root.new = true;
            $scope.$root.address = {
                province: '陕西省',
                city: '西安市',
                userid: User.current().id,
                tel: '',
                mobile: ''
            };
            $state.go('tab.address_edit');
        };
        $scope.changeRange = function () {
            $scope.$root.streets = MyAddress.getCurrentStreets($scope.$root.address.region);
            $scope.$root.address.street = "";
        };
        $scope.modifyAddress = function (id) {
            $scope.$root.new = false;
            $scope.$root.address = MyAddress.getAddressByID(id, User.current().addresses);
            $scope.changeRange();
            $state.go('tab.address_edit', {
                id: id
            });
        };
        $scope.setAsDefault = function (id) {
            Loading.show();
            var resource = $resource(config.domain + '/mobile/defaultaddress');
            resource.save({
                id: id
            }, function (data) {
                Loading.close();
                if (data.flag == 1) {
                    Loading.tip('设置成功');
                    MyAddress.setDefaultAddress(id, User.current().addresses);
                    $ionicHistory.goBack();
                } else {
                    Loading.tip(data.msg);
                }
            });
        };
        $scope.saveNewAddress = function () {
            Loading.show();
            var address = $scope.$root.address;
            address.tel = '';
            var resource = $resource(config.domain + '/mobile/addaddress');
            resource.save(address,
                function (data) {
                    Loading.close();
                    if (data.flag == 1) {
                        Loading.tip('保存成功');
                        MyAddress.newAddress(data.msg, User.current().addresses);
                        $ionicHistory.goBack();
                        $scope.$emit('address:saveNewSuccess', {
                            address: data.msg
                        });
                    } else {
                        Loading.tip(data.msg);
                    }
                },
                function () {
                    Loading.close();
                    Loading.tip('应用异常');
                });
        };
        $scope.saveModifyAddress = function () {
            Loading.show();
            var address = $scope.$root.address;
            var resource = $resource(config.domain + '/mobile/updateaddress');
            resource.save(address,
                function (data) {
                    Loading.close();
                    if (data.flag == 1) {
                        Loading.tip('保存成功');
                        MyAddress.updateAddress(address, User.current().addresses);
                        $ionicHistory.goBack();
                    } else {
                        Loading.tip(data.msg);
                    }
                },
                function () {
                    Loading.tip('应用异常');
                });
        };
        $scope.addressSubmit = function updateaddresson() {
            var address = $scope.$root.address;
            if (address.region && address.address && address.name && address.mobile) {
                if ($scope.new) {
                    $scope.saveNewAddress();
                } else {
                    $scope.saveModifyAddress();
                }
            } else {
                Loading.tip('地址信息输入不完整，请检查');
            }
        };
        $scope.deleteAddress = function (id) {
            Loading.show();
            var resource = $resource(config.domain + '/mobile/deladdress');
            resource.save({
                    id: id
                },
                function (data) {
                    Loading.close();
                    if (data.flag == 1) {
                        MyAddress.delAddress(id, $scope);
                        Loading.tip('删除成功');
                        $ionicHistory.goBack();
                    } else {
                        Loading.tip(data.msg);
                    }
                },
                function () {
                    Loading.close();
                    Loading.tip('应用异常');
                });
        };

        $scope.user = user;
        fetch();
    })
    /*Tabs control*/
    .controller('TabsCtrl', function ($scope, $state, ShopCar) {
        var resume = function () {
            $scope.carNumber = 0;
            var optionals = ShopCar.all();
            if (optionals) {
                $scope.carNumber += optionals.length;
            }

            var gifts = ShopCar.getGifts();
            if (gifts) {
                $scope.carNumber += gifts.length;
            }
        };

        $scope.$on('removeCar', function () {
            //$scope.cars = ShopCar.all().length;
            resume();
        });
        $scope.$on('putCar', function () {
            //$scope.cars = ShopCar.all().length;
            resume();
        });
        $scope.$on('user:updateProfileSuccess', function () {
            resume();
        });

        resume();
    })
    .controller('SearchResultCtrl', function ($scope, $state, $resource, Loading, SearchKeywords) {
        $scope.keyword = $state.params.keyword;
        $scope.searchProduct = function () {
            if ($scope.keyword.length > 0) {
                SearchKeywords.add($scope.keyword);
                Loading.show();
                var searchHelper = $resource(config.domain + '/mobile/search');
                searchHelper.query({
                        keywords: $scope.keyword
                    },
                    function (data) {
                        Loading.close();
                        $scope.products = _.map(data, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                    },
                    function (data) {
                        Loading.tip('应用异常');
                        console.log(data);
                    });

            } else {
                Loading.tip('请输入要搜索的产品名称');
            }
        };
        $scope.showDetail = function (id) {
            $state.go('tab.home-product', {
                id: id
            });
        };
        $scope.searchProduct();
    })
    .controller('SearchResultCtrl', function ($scope, $state, $resource, Loading, SearchKeywords) {
        $scope.keyword = $state.params.keyword;
        $scope.searchProduct = function () {
            if ($scope.keyword.length > 0) {
                SearchKeywords.add($scope.keyword);
                Loading.show();
                var searchHelper = $resource(config.domain + '/mobile/search');
                searchHelper.query({
                        keywords: $scope.keyword
                    },
                    function (data) {
                        Loading.close();
                        $scope.products = _.map(data, function (item) {
                            item.img = config.domain + '/upload/' + item.sku + '/' + item.cover;
                            return item;
                        });
                    },
                    function (data) {
                        Loading.tip('应用异常');
                        console.log(data);
                    });

            } else {
                Loading.tip('请输入要搜索的产品名称');
            }
        };
        $scope.showDetail = function (id) {
            $state.go('tab.home-product', {
                id: id
            });
        };
        $scope.searchProduct();
    })
    .controller('GiftsCtrl', function ($scope, $state, $http, Loading, SearchKeywords, User) {
        $scope.loadMore = function () {

            var user = User.current();

            $http
                .get(config.domain + '/mobile/gifts', {
                    params: {
                        userid: user.id
                    }
                })
                .success(function (res) {
                    $scope.hasMore = false;
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    if (res && res.flag === 1) {
                        //$scope.$apply(function () {
                        $scope.gifts = _.map(res.gifts, function (gift) {
                            gift.expirs = gift.expirs * 1000;
                            return gift;
                        });
                        // });
                    }
                })
                .catch(function (error) {
                    $scope.$broadcast('scroll.infiniteScrollComplete');
                    $scope.hasMore = false;
                    cosole.log(error);
                });
        };
        $scope.switch = function (choose) {
            $scope.choose = choose;
        };
        $scope.showDetail = function (id) {
            $state.go($state.$current.name + '-product', {
                id: id
            });
        };
        $scope.now = parseInt(new Date().getTime());
        $scope.config = config;
        $scope.gifts = [];
        $scope.choose = 'unused';
        $scope.hasMore = true;
    })
    .controller('NearbyCtrl', function ($scope, $state, $base64, $http, $ionicHistory, $timeout, Loading, User) {
        var locationSuccess = function (position) {
                var currentLat = position.coords.latitude;
                var currentLon = position.coords.longitude;

                $http
                    .get("http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=" + currentLon + "&y=" + currentLat)
                    .success(function (result) {
                        var location = {
                            x: $base64.decode(result.x),
                            y: $base64.decode(result.y)
                        };

                        Map.setMainLocation($scope.map, location);
                        Map.center($scope.map, location);
                    })
                    .catch(function (error) {
                        console.log(result);
                    });


            },
            locatinoFail = function (err) {
                //$scope.position = 'error';
            };

        $scope.clear = function () {
            $ionicHistory.goBack();
            //$timeout(function () {
            $scope.$root.$broadcast('store:clearDefaultSuccess');
            //}, 500);
        };
        $scope.map = null;
        $scope.$on('$ionicView.afterEnter', function () {
            if (!$scope.map) {
                Loading.show();
                $http
                    .get(config.domain + '/mobile/stores')
                    .success(function (result) {
                        Loading.close();
                        $scope.map = Map.instance('nearby_map');
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(locationSuccess, locatinoFail);
                        }

                        _.each(result.data, function (item) {
                            Map.addStoreOverlay($scope.map, item);
                        });

                    })
                    .catch(function (error) {
                        Loading.tip('应用异常');
                        console.log(error);
                    });
            }
        });
        $scope.$on('map:clickStoreOverlay', function (event, args) {

            localStorage.storeID = args.store.id;
            localStorage.storeName = args.store.name;
            $scope.$root.$broadcast('store:requestRefreshCategory', {
                store: args.store
            });

            $state.go($state.params.from + '-store-categories', {
                from: $state.params.from
            });
        });
    })
    .controller('PresaleCtrl', function ($scope, $state, $http, Loading, User, ShopCar) {
        $scope.item = ShopCar.getPresaleForDetail();
        $scope.addQuantity = function (num) {
            $scope.quantity = $scope.quantity + num;
        };
        $scope.buyPresale = function () {
            var user = User.current(),
                item = $scope.item;

            if (!user) {
                return $scope.$emit('user:requireLogin');
            }

            if (item) {
                ShopCar.put({
                    pid: item.pid,
                    checked: true,
                    quantity: $scope.quantity,
                    price: item.price,
                    psid: item.id,
                    type: 2
                });

                Loading.tip('已加入到购物车');
                if (user) {
                    ShopCar.upload(user.id, ShopCar.all());
                }
            }
        };
        $scope.quantity = 1;
    })
    .controller('TradeCtrl', function ($scope, $state, $resource, $ionicHistory, Loading, User) {
        var user = User.current();
        $scope.score = user.score;
        $scope.products = [];

        $scope.back = function () {
            $ionicHistory.goBack();
        }
    })
    .controller('StoreCategories', function ($scope, $state, $http, $ionicHistory, $location, $timeout, Loading, $ionicScrollDelegate, ShopCar, User) {
        var storeID = localStorage.storeID,
            storeName = localStorage.storeName,
            fetch = function () {
                Loading.show();
                $http
                    .get(config.domain + '/mobile/store/category/' + storeID)
                    .success(function (result) {
                        Loading.close();
                        $scope.categories = result.data;
                        //$scope.storeName = storeName + ' ';

                        if (result.data && result.data.length > 0) {
                            var choose = _.find(result.data, function (item) {
                                return item.code == $state.params.selected;
                            });

                            if (!choose) {
                                choose = _.find(result.data, function (item) {
                                    return (item && item.code && item.code.length === 4);
                                });
                            }

                            if (!choose) {
                                choose = {
                                    name: '全部',
                                    code: ''
                                }
                            }

                            $scope.choose = choose.name;
                            $scope.showProduct(choose.code, choose.name);
                        } else {
                            $scope.choose = '全部';
                            $scope.showProduct('', '全部');
                        }
                    }
                )
                    .catch(function (error) {
                        Loading.tip('应用异常');
                        console.log(error);
                    });
            };
        $scope.getStoreName = function () {
            return storeName + 'bbb';
        };
        $scope.$on('$ionicView.afterEnter', function () {
            if (!storeID) {
                return $state.go('tab.nearby', {
                    from: 'tab.categories'
                });
            }
        });
        $scope.$root.$on('store:requestRefreshCategory', function (event, args) {
            storeID = args.store.id;
            storeName = args.store.name;

            $timeout(function () {
                $scope.$apply(function () {
                    $scope.storeName = storeName + ' ';
                });
            }, 1000);

            fetch();
        });
        $scope.buy = function (id) {
            var exist = _.find($scope.products, function (product) {
                    return product.psid === parseInt(id);
                }),
                user = User.current();

            if (exist) {
                exist.quantity = 1;
                exist.storeid = parseInt(storeID);
                ShopCar.put({
                    pid: exist.pid,
                    psid: exist.psid,
                    quantity: 1,
                    product: exist,
                    checked: true,
                    limit: exist.limit,
                    renaming: exist.renaming
                });

                if (user) {
                    ShopCar.upload(user.id, ShopCar.all());
                }

                Loading.tip('已放入购物车', 1000);
            }
        };
        $scope.addQuantity = function (psid, count) {
            var exist = _.find($scope.products, function (product) {
                    return product.psid === parseInt(psid);
                }),
                user = User.current();

            if (exist) {
                var quantity = exist.quantity + count;
                if (quantity <= 0) {
                    quantity = 1;
                }

                if (quantity >= 5) {
                    quantity = 5;
                }

                exist.quantity = quantity;

                ShopCar.put({
                    pid: exist.pid,
                    psid: psid,
                    quantity: exist.quantity,
                    product: exist,
                    checked: true,
                    limit: exist.limit,
                    renaming: exist.renaming
                });

                if (user) {
                    ShopCar.upload(user.id, ShopCar.all());
                }
            }
        };
        $scope.config = config;
        $scope.showProduct = function (code, name) {
            $location.hash(code);
            $timeout(function () {
                $ionicScrollDelegate.$getByHandle('categoriesNameScroll').anchorScroll(code);
                $ionicScrollDelegate.$getByHandle('categoriesProductScroll').scrollTop();
            }, 1000);

            Loading.show();
            $scope.choose = name;


            $http
                .get(config.domain + '/mobile/store/product/' + storeID + '?code=' + code)
                .success(function (result) {
                    Loading.close();
                    if (result) {
                        $scope.products = result;
                    }
                })
                .catch(function (error) {
                    Loading.tip('应用异常');
                    console.log(error);
                });
        };
        $scope.switch = function () {
            $state.go($state.params.from + '-nearby', {
                from: $state.params.from
            });
        };
        $scope.storeName = storeName;
        $scope.showProductDetail = function (psid) {
            $state.go($state.$current.name + '-product', _.extend($state.params, {
                id: psid
            }));
        };
        $scope.$root.$on('store:clearDefaultSuccess', function () {
            $timeout(function () {
                $ionicHistory.goBack();
            }, 1000);
        });

        fetch();
    });