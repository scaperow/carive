angular
  .module('starter.controllers', ['ngResource', 'pasvaz.bindonce', 'base64'])
  /*
   程序入口
   */
  .run(function($rootScope, $state, $q, $ionicPopup, $ionicLoading, $resource, $http, $stateParams, $ionicPopup, $location, $ionicPlatform, $ionicHistory, $ionicModal, $window, $timeout, User, Loading) {
    // window.plugins.share({
    //  title:'sdfadsfadf',
    //  id:'adfadsfadf',
    //  context:'sfafdasdfadf'
    // });
    $window.addEventListener('online', function() {
      $rootScope.offline = false;
      $ionicLoading.hide();
    });
    $window.addEventListener('offline', function() {
      $rootScope.offline = true;
      $ionicLoading.show({
        template: '没有网络不能操作'
      });
    });
    $rootScope.closeLogin = function() {
      $rootScope.loginModal.hide();
      //var back = $ionicHistory.backView();
      $state.transitionTo($state.current, $stateParams, {
        reload: true,
        inherit: false,
        notify: true
      });
    };
    $rootScope.call = function(tel) {
      window.location.href = 'tel://' + tel;
    };
    $rootScope.changeStatus = function(status) {
      $rootScope.registerModel = {};
      $rootScope.resetPasswordModel = {};
      $rootScope.loginModalStatus = status;
    };
    $rootScope.requestCodeWithRegister = function() {
      var userName = $rootScope.registerModel.userName + '';
      if (userName.length != 11) {
        return Loading.tip('请输入正确的手机号码');
      }

      User.requestValidationCodeRegister(userName)
        .then(function(result) {
          $rootScope.counterWithRequestCode = 60;
          $rootScope.requestCodeProcessing = true;

          var loop = function() {
            if (--$rootScope.counterWithRequestCode <= 0) {
              $rootScope.counterWithRequestCode = 60;
              $rootScope.requestCodeProcessing = false;
            } else {
              $timeout(loop, 1000);
            }
          };

          loop();
        })
        .catch(function(error) {
          if (error.message) {
            Loading.tip(error.message);
          }
        });
    };
    $rootScope.requestCodeWithRecovery = function() {
      var userName = $rootScope.resetPasswordModel.userName + '';

      if (userName.length != 11) {
        return Loading.tip('请输入正确的手机号码');
      }

      User.requestValidationCodeRecovery(userName)
        .then(function(result) {
          $rootScope.requestCodeProcessing = true;
          $rootScope.counterWithRequestCode = 60;

          var loop = function() {
            if (--$rootScope.counterWithRequestCode <= 0) {
              $rootScope.counterWithRequestCode = 60;
              $rootScope.requestCodeProcessing = false;
            } else {
              $timeout(loop, 1000);
            }
          };

          loop();
        })
        .catch(function(error) {
          if (error.message) {
            Loading.tip(error.message);
          }
        });
    };
    $ionicModal
      .fromTemplateUrl('templates/login.html', {
        scope: $rootScope
      })
      .then(function(modal) {
        $rootScope.loginModal = modal;
      });

    $ionicModal
      .fromTemplateUrl('templates/xieyi.html', {
        scope: $rootScope
      })
      .then(function(modal) {
        $rootScope.xieyiModal = modal;
      });
    $rootScope.aggreeXieYi = function() {
      $rootScope.xieyi = true;
    };
    $rootScope.closeXieYi = function() {
      $rootScope.xieyiModal.hide();
    };
    $rootScope.showXIEYI = function() {
      $rootScope.xieyiModal.show();
    };
    $rootScope.unaggreeXieYi = function() {
      $rootScope.xieyi = false;
    };
    $rootScope.loginWithQQ = function() {
      Loading.show();

      User
        .loginWithQQ()
        .then(function() {
          Loading.close();
          User.syncProfile();

          $rootScope.loginModal.hide();
        })
        .catch(function(error) {
          if (error) {
            Loading.tip(error);
          }
        });
    };
    $rootScope.register = function() {
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
            function(data) {
              Loading.close();

              if (data.flag == 1) {

                $rootScope.loginModal.hide();
                localStorage["username"] = $rootScope.registerModel.userName;
                localStorage["password"] = hex_md5($rootScope.registerModel.password);
                User.valided();
                User.setUser(data['msg']);
                //$state.go('tab.account');
                $rootScope.$broadcast('registSuccess');
              } else {
                Loading.tip(data['msg']);
              }

              $rootScope.registerModel.password = '';
              $rootScope.registerModel.repassword = '';
            },
            function(error) {
              Loading.tip(error.data.msg);
              $rootScope.registerModel.password = '';
              $rootScope.registerModel.confirmPassword = '';
            });
        } else {
          Loading.tip('两次密码输入不一致，请重新输入');
        }
      } else {
        Loading.tip('注册信息输入不完整，请检查');
      }
    };
    $rootScope.login = function() {
      if ($rootScope.loginModel.userName && $rootScope.loginModel.password) {
        Loading.show();

        User
          .login($rootScope.loginModel.userName, hex_md5($rootScope.loginModel.password))
          .then(function() {
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
              //$state.go('tab.account');
            }
          });
      } else {
        Loading.tip('请输入用户名和密码');
      }
    };
    $rootScope.$on('$stateChangeStart',
      function(event, toState, toParams, fromState, fromParams) {
        var validate = function() {
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
          hideTabs = function() {
            var deferred = $q.defer();
            if (toState.hideTabs) {
              $rootScope.tohide = "tabs-item-hide";
            } else {
              $rootScope.tohide = "";
            }

            deferred.resolve();
            return deferred.promise;
          },
          networkDetect = function() {
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
          .catch(function(err) {
            console.log(err);
          });
      }
    );

    $rootScope.$on('user:requireLogin', function(event, args) {
      Loading.tip('请您登录');
      $rootScope.loginModal.show();
      // $rootScope.loginDeferred = args.deferred;
      $rootScope.recoveryPasswordOnly = false;
      $rootScope.loginModalStatus = 'LOGIN';
    });
    $rootScope.$on('http:errorResponse', function(event, args) {
      Loading.tip(args.message);
    });
    $rootScope.$on('http:exceptionRespons', function(event, args) {
      Loading.tip(args.message);
    });
    $rootScope.validateCode = function() {
      if (!$rootScope.resetPasswordModel.userName) {
        return Loading.tip('请输入手机号码');
      }

      if (!$rootScope.resetPasswordModel.validationCode) {
        return Loading.tip('请输入验证码 ');
      }

      User.requestResetPassword($rootScope.resetPasswordModel.validationCode, $rootScope.resetPasswordModel.userName)
        .then(function(result) {
          var userName = $rootScope.resetPasswordModel.userName;
          $rootScope.changeStatus('RESETPASSWORD');
          $rootScope.resetPasswordModel.userName = userName;
        })
        .catch(function(error) {
          Loading.tip(error.message);
        });
    };
    $rootScope.resetPassword = function() {
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
        .then(function(result) {
          Loading.tip('您的密码已修改');
          $rootScope.resetPasswordModel = {};
          $rootScope.loginModal.hide();
          $rootScope.changeStatus('LOGIN');
          //$state.go('tab.account');
        })
        .catch(function(error) {
          Loading.tip(error.message);
        });
    };
    $rootScope.$on('loginSuccess', function(event, user) {
      $rootScope.user = user;
    });
    $rootScope.recoverPassword = function() {
      $rootScope.loginModalStatus = 'RECOVERPASSWORD';
    };
    $ionicPlatform.ready(function() {

      var setTagsWithJPush = function(tags, alias) {
        if (window.plugins && window.plugins.jPushPlugin) {
          window.plugins.jPushPlugin.setTagsWithAlias(tags, alias);
        }
      };

      $rootScope.$on('loginSuccess',
        function(event, user) {
          var tags = ['user'],
            alias = user.mobile;

          if (user.mobile == '13239109398') {
            tags.push('administrator');
          }

          setTagsWithJPush(tags, alias);
        });

      if (window.plugins && window.plugins.jPushPlugin) {
        window.plugins.jPushPlugin.init();
      }

      // try {
      //   $sharesdk.open("iosv1101", true);
      //
      //   var sinaConf = {};
      //   sinaConf["app_key"] = "c9cbbb650e0e";
      //   sinaConf["app_secret"] = "3461b79725018ba738adda09cdf42cce";
      //   sinaConf["redirect_uri"] = "http://www.sharesdk.cn";
      //   $sharesdk.setPlatformConfig($sharesdk.platformID.SinaWeibo, sinaConf);
      //
      //   var params = {
      //     "text": "测试的文字",
      //     "imageUrl": "http://img0.bdstatic.com/img/image/shouye/tangwei.jpg",
      //     "title": "测试的标题",
      //     "titleUrl": "http://sharesdk.cn",
      //     "description": "测试的描述",
      //     "site": "ShareSDK",
      //     "siteUrl": "http://sharesdk.cn",
      //     "type": $sharesdk.contentType.Text
      //   };
      //
      //   $sharesdk.shareContent($sharesdk.platformID.SinaWeibo, params, function(platform, state, shareInfo, error) {
      //     alert("state = " + state + "\nshareInfo = " + shareInfo + "\nerror = " + error);
      //   });
      // } catch (e) {
      //   console.log(e);
      // }
    });
    $rootScope.previewImage = function(url) {
      $rootScope.imageSrc = url;
      $rootScope.previewImageModal.show();
    };
    $rootScope.closePreviewModal = function() {
      $rootScope.previewImageModal.hide();
    };

    $ionicModal
      .fromTemplateUrl('templates/img-modal.html', {
        scope: $rootScope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $rootScope.previewImageModal = modal;
      });


    User.loginBackend();
    $rootScope.loginModalStatus = 'LOGIN';
    $rootScope.resetPasswordModel = {};
    $rootScope.loginModel = {};
    $rootScope.registerModel = {};
    $rootScope.tab = 0;
    $rootScope.xieyi = true;
  })
  .controller('IndexCtrl', function($scope, $ionicTabsDelegate, $ionicSideMenuDelegate, $http, $state, ShopCar, Loading, User) {
    var resumeShopCarNumber = function() {
      $scope.$root.carNumber = ShopCar.all().length;
      // $scope.carNumber = new Date();
    };
    $scope.tab = 0;
    $scope.category = null;
    $scope.switch = function(tab) {
      index = tab;

      switch (tab) {
        case 0:
          $scope.$root.$broadcast('tab:changeToHome');
          break;

        case 1:
          break;

        case 2: //shop car
          $scope.$root.$broadcast('tab:changeToCart');

          break;

        case 3:
          if (!$scope.$root.user) {
            index = $scope.tab;
            $scope.$emit('user:requireLogin');
          }
          break;
      }

      $ionicTabsDelegate.select(index);
      $scope.tab = index;
    };
    $scope.showOtherService = function() {
      $state.go('services-category');
    };
    $scope.showProductSearch = function() {
      $state.go('search');
    };
    $scope.setLocation = function() {
      $state.go('regions');
    };
    $scope.$root.$on('user:logoutSuccess', function(event, user) {
      $scope.switch(0);
      $scope.$root.user = null;
    });
    $scope.$on('user:updateProfileSuccess', function() {
      resumeShopCarNumber();
    });
    $scope.$on('shopCar:addItemSuccess', function() {
      resumeShopCarNumber();
    });
    $scope.$on('shopCar:removeItemSuccess', function() {
      resumeShopCarNumber();
    });
  })
  /*
   添加评论路由
   */
  .controller('CommentCtrl', function($http, $resource, $scope, $http, $state, $ionicHistory, Loading, User) {
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
    $scope.rateProduct = function(rate) {
      $scope.comment.productRate = rate;
    }
    $scope.rateSpeed = function(rate) {
      $scope.comment.speedRate = rate;
    };
    $scope.ratePrice = function(rate) {
      $scope.comment.priceRate = rate;
    }
    $scope.rateService = function(rate) {
      $scope.comment.serviceRate = rate;
    }
    $scope.save = function() {
      var comment = $scope.comment;
      if (!comment.content) {
        return Loading.tip('请填些评价内容', 1200);
      }

      var resource = $resource(config.domain + '/mobile/comment/add');
      resource.save(comment,
        function() {
          Loading.tip('您已评价，谢谢');
          var user = User.current();
          var resource = $resource(config.domain + '/mobile/payinfo');

          resource.get({
              userid: user.id,
              price: -1
            },
            function(result) {
              user.addresses = result.address;
              user.balance = result.balance;
              user.score = result.score;
            },
            function(error) {
              console.log(error);
            });

          $scope.$root.$broadcast('comment', {
            comment: comment
          });
          $ionicHistory.goBack();
        },
        function() {
          Loading.tip('应用发生异常');
          console.log(result);
        });
    };
  })
  /*
   评论列表路由
   */
  .controller('CommentsCtrl', function($http, $resource, $scope, $state, $ionicScrollDelegate, User, Loading) {
    var refresh = function() {
      var resource = $resource(config.domain + '/mobile/comment/list');
      resource.get({
          userId: $scope.userId,
          psid: $scope.psid,
          index: $scope.index,
          size: $scope.size
        },
        function(result) {

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
            $scope.$broadcast('scroll.infiniteScrollComplete');
        },
        function(err) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          console.log(err);
        });

    };

    $scope.index = $scope.index || 1;
    $scope.size = $scope.size || 20;
    $scope.psid = $state.params.psid;
    $scope.load = function() {
      refresh();
    };
    $scope.hasMore = true;
  })
  /*首页control*/
  .controller('HomeCtrl', function($scope, $resource, $state, $ionicPopup, $ionicListDelegate, $window, $filter, $timeout, $http, $location, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $ionicScrollDelegate, $q, Location, Ad, Products, Loading, SearchKeywords, User, ShopCar) {
    var fetchHome = function() {
        return Products.refresh();
      },
      fetchAuto = function() {
        Loading.show();
        var deferred = $q.defer();
        var user = User.current();
        if (user) {
          $http
            .get(config.domain + '/mobile/get_auto', {
              params: {
                uid: user.id
              }
            })
            .success(function(result) {
              Loading.close();
              $scope.auto = result.msg || {
                'auto_id': null,
                'mileage': null,
                'buy_time': null,
                'chassis_num': null,
                'car_num': null,
                'brand_code': null,
                'brand_id': null,
                'created': null,
                'brand': []
              };
              $scope.brand = _.pluck(result.msg.brand, 'name').join(' ');
              deferred.resolve();
            });
        } else {
          deferred.resolve();
        }
        Loading.close();
        return deferred.promise;
      },
      fetchQuestions = function() {
        var deferred = $q.defer();
        var user = User.current();
        if (user) {
          Loading.show();
          $http
            .get(config.domain + '/mobile/question', {
              params: {
                size: 3
              }
            })
            .success(function(result) {

              $scope.questions = _.map(result.questions, function(question) {
                if (question.user_photo) {
                  question.user_photo = config.domain + question.user_photo;
                }

                var bests = _.where(result.bests, {
                  question_id: question.id
                });

                if (bests.length > 0) {
                  question.best = bests[0];
                  if (bests[0].user_photo) {
                    bests[0].user_photo = config.domain + bests[0].user_photo;
                  }
                }

                return question
              });

              deferred.resolve();
            })
            .catch(function() {
              deferred.resolve();
            });
        } else {
          deferred.resolve();
        }

        return deferred.promise;
      },
      fetchAds = function() {
        var deferred = $q.defer();
        var ads = [];

        Ad
          .fetch()
          .then(function(result) {
            ads = result;
            $scope.loading = true;
            $timeout(function() {
              //腰部广告
              $scope.ads = _.where(ads, {
                atype: 3
              });
              //顶部广告
              $scope.banner = _.where(ads, {
                atype: 4
              });
              //推荐
              $scope.recommands = _.where(ads, {
                atype: 5
              });
              var handler = $ionicSlideBoxDelegate.$getByHandle('slide-ads');

              if (handler) {
                handler.update();
              }

              handler = $ionicSlideBoxDelegate.$getByHandle('slide-banner');

              if (handler) {
                handler.update();
              }

              handler = $ionicSlideBoxDelegate.$getByHandle('slide-recommands');

              if (handler) {
                handler.update();
              }

              $scope.loading = false;
            }, 1000);

            deferred.resolve();
          })
          .catch(function(error) {
            //如果获取广告失败，依然通过
            deferred.resolve();
          });

        return deferred.promise;
      },
      fetchHistory = function() {
        var user = User.current(),
          deferred = $q.defer();

        if (user) {
          $http
            .get(config.domain + '/mobile/get_browse/' + user.id)
            .success(function(result) {
              if (result) {
                $scope.histories = _.map(result, function(item) {
                  item.cover = config.domain + item.cover;
                  return item;
                });
              }
              deferred.resolve();
            })
            .catch(function(error) {
              deferred.resolve();
            });
        } else {
          deferred.resolve();
        }

        return deferred.promise;
      },
      fetchRecommand = function(id) {
        var user = User.current(),
          city = User.getCity(),
          deferred = $q.defer();

        if (city) {
          $http
            .get(config.domain + '/mobile/product_recommend', {
              params: {
                cityid: city.id
              }
            })
            .success(function(result) {
              $scope.recommands = _.map(result, function(item) {
                item.cover = config.domain + item.cover;
                return item;
              });

              deferred.resolve();
            })
            .catch(function() {
              deferred.resolve();
            });
        } else {
          deferred.resolve();
        }

        return deferred.promise;
      };
    $scope.message = function() {
      $state.go('message');
    };
    //求助服务
    $scope.helpService = function() {
      var user = User.current();
      if (!user) {
        return $scope.$emit('user:requireLogin');
      }

      var location = User.getLocation();
      if (location) {
        Loading.show();
        uid = '';
        if (user) {
          uid = user.id
        }

        $http
          .get(config.domain + '/mobile/store_tel', {
            params: {
              x: location.x,
              y: location.y,
              category: '',
              order: 'distance',
              area: '',
              uid: uid
            }
          })
          .then(function(result) {
            Loading.close();
            if (result.data.flag == 1) {
              $scope.$root.call(result.data.data.tel);
            } else {
              Loading.tip('抱歉，附近没有商家信息');
            }
          })
      } else {
        Loading.tip('当前没有您的坐标信息，请稍后再试');
      };
    }
    $scope.$root.$on('loginSuccess', function() {
      var user = User.current();
      if (user) {
        $scope.score = user.score
      } else {
        $scope.score = null;
      }

      Loading.show();
      fetchQuestions()
        .then(function() {
          Loading.close();
        });
    });
    $scope.$root.$on('user:tradeSuccess', function(event, args) {
      $scope.score = args.user.score;
    });
    $scope.$on('$ionicView.afterEnter', function() {
      $ionicSlideBoxDelegate.$getByHandle('slide-banner').update();
    });
    $scope.$on('tab:changeToHome', function() {
      $ionicSlideBoxDelegate.update();
    });
    $scope.$root.$on('store:clearDefaultSuccess', function() {
      $timeout(function() {
        localStorage.storeID = localStorage.storeName = '';
      }, 1500);
    });
    $scope.$root.$on('location:setCity', function(event, args) {
      $scope.city = args.city;
      $scope.refresh(true);
    });
    $scope.showProduct = function(id) {
      $state.go('product', {
        id: id
      });
    };
    $scope.titleClick = function(type) {
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
    $scope.search = function() {
      $state.go('search');
    };
    $scope.docker = function(id) {
      var ad = Ad.get(id);
      if (ad) {
        switch (ad.href.key) {
          case '1':
            $state.go('product', {
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
            $scope.$root.loginModalStatus = 'REGISTER';
            $scope.$root.loginModal.show();
            break;
        }
      }
    };
    $scope.setLocation = function() {
      $state.go('regions');
    };
    $scope.refresh = function(shouldNotLoading) {
      if (!shouldNotLoading) {
        Loading.show();
      }

      $q
        .all([fetchHome(), fetchAds(), fetchRecommand(), fetchQuestions()])
        .then(function() {
          $ionicScrollDelegate.resize();
          $scope.$broadcast('scroll.refreshComplete');
          Loading.close();
        });
    };
    $scope.$on('loginSuccess', function() {
      fetchAuto();
    });
    $scope.showPresaleDetail = function(id) {
      var exist = _.find($scope.pre_sales, function(item) {
        return (item.id === parseInt(id));
      });

      if (exist) {
        ShopCar.setPresaleForDetail(exist);
        $state.go('tab.pre-sale-detail');
      }
    };
    $scope.showStore = function(id) {
      $state.go('store', {
        id: id
      });
    };
    $scope.searchStore = function() {
      $state.go('stores');
    };
    $scope.showCategory = function(code) {
      //$state.go('categories', {code: code});
      $state.go('categories', {
        keyword: code
      });
    };
    $scope.showPeccancy = function() {
      $state.go('peccancy');
    };
    $scope.showAllService = function() {
      $state.go('services-category');
    };
    $scope.showParkCar = function() {
      $state.go('park');
    };
    $scope.showGasStation = function() {
      $state.go('gas-station');
    }
    $scope.showType = function(code) {
      $state.go('categories', {
        type: code
      });
    };
    $scope.addMineCar = function() {
      $state.go('profile');
    }
    var city = User.getCity();
    if (city) {
      $scope.city = city;
      $scope.refresh();
      Location
        .current()
        .then(function(location) {
          User.setLocation(location);
        });
    } else {
      Location
        .current()
        .then(function(location) {
          User.setLocation(location);
          $http
            .get(config.domain + '/mobile/select_city')
            .success(function(result) {
              city = _.find(result, function(item) {
                return item.name === location.address.city
              });

              User.setCity(city);
              $scope.city = city;
              $scope.refresh();
            })
            .error(function() {
              Loading.tip('请设置您的位置');
              $state.go('regions');
            });
        })
        .then(null, function(err) {
          Loading.tip('请设置您的位置');
          $state.go('regions');
        });
    }
  })
  .controller('MessageCtrl', function($scope, $state, $ionicScrollDelegate, $ionicPopup, $http, User, Loading) {
    var max = 9999999999999;
    $scope.fetch = function() {
      $scope.hasMore = false;
      Loading.show();
      $http
        .get(config.domain + '/mobile/messages', {
          params: {
            uid: $scope.$root.user.id,
            max: max,
            size: 20
          }
        })
        .success(function(result) {

          if (result && result.msg.length > 0) {
            max = result.msg[result.msg.length - 1].id;
            $scope.messages = _.union($scope.messages, result.msg);
            $scope.hasMore = true;
          } else {
            $scope.total = 0;
          }

          Loading.close();
          $scope.$broadcast('scroll.infiniteScrollComplete');

        })
        .catch(function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          console.log(error);
        });
    };

    $scope.showDetail = function(id) {
      var exists = _.find($scope.messages, function(message) {
        return message.id === parseInt(id)
      });

      if (exists) {
        exists.has_read = 1;
      }

      $state.go("message-detail", {
        id: exists.id
      });
    };

    $scope.clear = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '您是否要清空所有消息？',
        scope: $scope,
        buttons: [{
          text: '是',
          type: 'button-balanced',
          onTap: function(e) {
            Loading.show();

            $http
              .post(config.domain + '/mobile/message_clear', {
                uid: $scope.$root.user.id
              })
              .success(function() {
                $scope.messages = [];
                Loading.close();
              })
          }
        }, {
          text: '否'
        }]
      });
    }

    $scope.hasMore = true;

  })
  .controller('MessageDetailCtrl', function($scope, $state, $ionicScrollDelegate, $http, User, Loading) {
    Loading.show();
    $scope.fetch = function() {
      $scope.hasMore = false;

      $http
        .post(config.domain + '/mobile/messages_detail', {
          id: $state.params.id,
          mark: true
        })
        .success(function(result) {
          Loading.close();
          $scope.message = result.msg;
        })
        .catch(function(error) {
          console.log(error);
        });
    };

    $scope.fetch();
  })
  .controller('CircleCtrl', function($scope, $state, $ionicScrollDelegate, $ionicPopup, $http, Loading, User) {
    var max = null,
      min = null,
      size = 10;

    $scope.$root.$on('topic:leaveReplySuccess', function(event, args) {
      var exists = _.find($scope.circleTopics, function(topic) {
        return topic.id == args.id
      });

      if (exists) {
        exists.replies.push(args);
      }
    });
    $scope.clickPraise = function(id) {
      var user = User.current();
      if (user) {
        $http
          .post(config.domain + '/mobile/leave-topic-praise', {
            id: id,
            uid: user.id
          })
          .success(function(result) {
            var exists = _.find($scope.circleTopics, function(topic) {
              return topic.id == id
            });

            if (exists) {
              exists.praises.push({
                user_name: user.username
              });
            }
          })
          .catch(function(error) {

          });
      } else {
        $scope.$emit('user:requireLogin');
      }
    };
    $scope.removePraise = function(id) {
      var confirmPopup = $ionicPopup.confirm({
        title: '您确定要删除吗？',
        cancelText: '取消',
        okText: '确定'
      });

      confirmPopup.then(function(res) {
        if (res) {
          var user = User.current();
          if (user) {
            $http
              .post(config.domain + '/mobile/remove-topic', {
                id: id,
                uid: user.id
              })
              .success(function(result) {
                $scope.circleTopics = _.reject($scope.circleTopics, function(i){
                  return i.id === id;
                });

                Loading.tip('已删除');
              })
              .catch(function(error) {
                Loading.tip('删除失败');
              });
          }
        }
      });
    };
    $scope.leaveReply = function(id, repliedUserName, repliedUserID, replyID) {
      var user = User.current();
      if (user) {
        if (repliedUserID !== user.id) {
          $state.go('leave-reply', {
            id: id,
            repliedUserName: repliedUserName,
            repliedUserID: repliedUserID
          });
        } else {
          $scope.removeModal = $ionicPopup.show({
            template: '是否要删除条评论?',
            scope: $scope,
            buttons: [{
              text: '是',
              type: 'button-balanced',
              onTap: function(e) {
                Loading.show();

                $http
                  .post(config.domain + '/mobile/delete_replay', {
                    id: replyID
                  })
                  .success(function(result) {
                    if (result.flag === 1) {
                      var exists = _.find($scope.circleTopics, function(topic) {
                        return topic.id == id
                      });

                      if (exists) {
                        exists.replies = _.reject(exists.replies, function(reply) {
                          return (reply.id === replyID);
                        });
                      }
                    }
                    Loading.close();
                  })
              }
            }, {
              text: '否'
            }]
          });
        }
      } else {
        $scope.$emit('user:requireLogin');
      }
    };
    $scope.fetch = function() {
      $http
        .get(config.domain + '/mobile/get_circle_topics', {
          params: {
            size: size,
            min: min || 999999999999
          }
        })
        .success(function(result) {
          if (result.msg.topics.length > 0) {
            var topics = _.map(result.msg.topics, function(topic) {
              topic.pictures =
                _.map(
                  _.where(result.msg.pictures, {
                    topic_id: topic.id
                  }),

                  function(picture) {
                    picture.path = config.domain + picture.path;
                    return picture;
                  });

              topic.praises = _.where(result.msg.praises, {
                topic_id: topic.id
              });

              topic.replies = _.where(result.msg.replies, {
                topic_id: topic.id
              });

              return topic;
            });

            $scope.circleTopics = _.union(topics, $scope.circleTopics);
            var i = topics[topics.length - 1].id;
            if (!min || i < min) {
              min = i;
            }

            var m = topics[0].id;
            if (!max || m > max) {
              max = m;
            }

            $scope.hasMore = true;
          }
          $scope.$broadcast('scroll.refreshComplete');
        })
        .catch(function(error) {
          $scope.$broadcast('scroll.refreshComplete');
        });
    }
    $scope.load = function() {
      $scope.hasMore = false;
      $http
        .get(config.domain + '/mobile/get_circle_topics', {
          params: {
            size: size,
            max: max || 99999999999
          }
        })
        .success(function(result) {
          if (result.msg.topics.length > 0) {
            var topics = _.map(result.msg.topics, function(topic) {
              topic.pictures =
                _.map(
                  _.where(result.msg.pictures, {
                    topic_id: topic.id
                  }),

                  function(picture) {
                    picture.path = config.domain + picture.path;
                    return picture;
                  });

              topic.praises = _.where(result.msg.praises, {
                topic_id: topic.id
              });

              topic.replies = _.where(result.msg.replies, {
                topic_id: topic.id
              });

              return topic;
            });

            $scope.circleTopics = _.union($scope.circleTopics, topics);
            $scope.hasMore = true;
            var a = topics[0].id;
            if (a > max) {
              max = a;
            }

            var i = topics[topics.length - 1].id;
            if (i < min) {
              min = i;
            }

            $scope.hasMore = false;
          }

          $scope.$broadcast('scroll.infiniteScrollComplete');
        })
        .catch(function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
        });
    };

    $scope.hasMore = false;
    $scope.circleTopics = [];
    $scope.fetch();
  })
  .controller('MineShowOrderCtrl', function($scope, $state, $ionicPopup, $ionicScrollDelegate, $http, User, Loading) {
    var min = 99999999999999999999,
      size = 10;


    $scope.$root.$on('topic:leaveReplySuccess', function(event, args) {
      var exists = _.find($scope.circleTopics, function(topic) {
        return topic.id == args.id
      });

      if (exists) {
        exists.replies.push(args);
      }
    });
    $scope.removePraise = function(id) {
      var confirmPopup = $ionicPopup.confirm({
        title: '您确定要删除吗？',
        cancelText: '取消',
        okText: '确定'
      });

      confirmPopup.then(function(res) {
        if (res) {
          var user = User.current();
          if (user) {
            $http
              .post(config.domain + '/mobile/remove-topic', {
                id: id,
                uid: user.id
              })
              .success(function(result) {
                $scope.circleTopics = _.reject($scope.circleTopics, function(i){
                  return i.id === id;
                });

                Loading.tip('已删除');
              })
              .catch(function(error) {
                Loading.tip('删除失败');
              });
          }
        }
      });
    };
    $scope.clickPraise = function(id) {
      var user = User.current();
      if (user) {
        $http
          .post(config.domain + '/mobile/leave-topic-praise', {
            id: id,
            uid: user.id
          })
          .success(function(result) {
            var exists = _.find($scope.circleTopics, function(topic) {
              return topic.id == id
            });

            if (exists) {
              exists.praises.push({
                user_name: user.username
              });
            }
          })
          .catch(function(error) {

          });
      }
    };
    $scope.leaveReply = function(id, repliedUserName, repliedUserID, replyID) {
      var user = User.current();
      if (user) {
        if (repliedUserID !== user.id) {
          $state.go('leave-reply', {
            id: id,
            repliedUserName: repliedUserName,
            repliedUserID: repliedUserID
          });
        } else {
          $scope.removeModal = $ionicPopup.show({
            template: '是否要删除条评论?',
            scope: $scope,
            buttons: [{
              text: '是',
              type: 'button-balanced',
              onTap: function(e) {
                Loading.show();

                $http
                  .post(config.domain + '/mobile/delete_replay', {
                    id: replyID
                  })
                  .success(function(result) {
                    if (result.flag === 1) {
                      var exists = _.find($scope.circleTopics, function(topic) {
                        return topic.id == id
                      });

                      if (exists) {
                        exists.replies = _.reject(exists.replies, function(reply) {
                          return (reply.id === replyID);
                        });
                      }
                    }
                    Loading.close();
                  })
              }
            }, {
              text: '否'
            }]
          });
        }
      } else {
        $scope.$emit('user:requireLogin');
      }
    };
    $scope.load = function() {
      $scope.hasMore = false;

      $http
        .get(config.domain + '/mobile/get_circle_topics', {
          params: {
            size: size,
            min: min,
            uid: $scope.$root.user.id
          }
        })
        .success(function(result) {
          if (result.msg.topics.length > 0) {
            var topics = _.map(result.msg.topics, function(topic) {
              topic.pictures =
                _.map(
                  _.where(result.msg.pictures, {
                    topic_id: topic.id
                  }),

                  function(picture) {
                    picture.path = config.domain + picture.path;
                    return picture;
                  });

              topic.praises = _.where(result.msg.praises, {
                topic_id: topic.id
              });

              topic.replies = _.where(result.msg.replies, {
                topic_id: topic.id
              });

              return topic;
            });

            $scope.circleTopics = _.union($scope.circleTopics, topics);
            $scope.hasMore = true;

            var i = topics[topics.length - 1].id;
            if (i < min) {
              min = i;
            }
          }

          $scope.hasMore = false;

          $scope.$broadcast('scroll.infiniteScrollComplete');
        })
        .catch(function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
        });
    };

    $scope.$root.$on('postCircle', function() {
      var max = 0;
      if ($scope.circleTopics && $scope.circleTopics.length > 0) {
        max = $scope.circleTopics[0].id;
      }

      $http
        .get(config.domain + '/mobile/get_circle_topics', {
          params: {
            size: size,
            max: max,
            uid: $scope.$root.user.id
          }
        })
        .success(function(result) {
          if (result.msg.topics.length > 0) {
            var topics = _.map(result.msg.topics, function(topic) {
              topic.pictures =
                _.map(
                  _.where(result.msg.pictures, {
                    topic_id: topic.id
                  }),

                  function(picture) {
                    picture.path = config.domain + picture.path;
                    return picture;
                  });

              topic.praises = _.where(result.msg.praises, {
                topic_id: topic.id
              });

              topic.replies = _.where(result.msg.replies, {
                topic_id: topic.id
              });

              return topic;
            });

            $scope.circleTopics = _.union($scope.circleTopics, topics);
            $scope.hasMore = true;

          }

          $scope.hasMore = false;

          $scope.$broadcast('scroll.infiniteScrollComplete');
        })
        .catch(function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
        });
    });



    $scope.hasMore = true;
    $scope.circleTopics = [];
  })
  .controller('QuestionCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $http, Loading, User) {
    var fetch = function() {

      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .get(config.domain + '/mobile/question', {
            params: {
              userid: user.id
            }
          })
          .success(function(result) {
            $scope.questions = result.questions;
            _.each(result.questions, function(question) {
              var bests = _.where(result.bests, {
                question_id: question.id
              });
              if (question.user_photo) {
                question.user_photo = config.domain + question.user_photo;
              }
              if (bests.length > 0) {
                question.best = bests[0];

                if (question.best.user_photo) {
                  question.best.user_photo = config.domain + question.best.user_photo;
                }
              }


            });

            Loading.close();
          })
          .catch(function() {

          })
      }
    };

    fetch();


    $scope.$root.$on('addQuestion', function(event, args) {
      fetch();
    });
  })
  .controller('AnswerCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $http, Loading, User) {
    var fetch = function() {
      Loading.show();

      var user = User.current();
      if (user) {
        $http
          .get(config.domain + '/mobile/question_answer', {
            params: {
              uid: user.id,
              question_id: $state.params.questionID
            }
          })
          .success(function(result) {
            $scope.answers = result.answers;
            $scope.bests = result.bests;
            $scope.question = result.question;
            Loading.close();
          })
          .catch(function() {

          })
      } else {
        $scope.$emit('user:requireLogin');
      }
    };

    $scope.supportAnswer = function(answerID) {
      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .post(config.domain + '/mobile/support_answer', {
            uid: 1,
            answer_id: answerID
          })
          .success(function(result) {
            var exists = _.find(_.union($scope.answers), function(answer) {
              return answer.id === answerID;
            })

            if (exists) {
              exists.supports = result.supports;
            }

            var exists = _.find(_.union($scope.bests), function(answer) {
              return answer.id === answerID;
            })

            if (exists) {
              exists.supports = result.supports;
            }

            Loading.tip(result.msg);
          })
      }
    };

    fetch();
  })
  .controller('ShowOrderCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $ionicHistory, $http, Loading, User) {
    $scope.imgs = [];
    $scope.content = '';
    var sure_exit = false;
    $scope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
      if (sure_exit) {
        return;
      }

      event.preventDefault();
      $scope.removeModal = $ionicPopup.show({
        template: '是否要退出编辑?',
        scope: $scope,
        buttons: [{
          text: '是',
          type: 'button-balanced',
          onTap: function(e) {
            sure_exit = true;
            $ionicHistory.goBack();
          }
        }, {
          text: '否'
        }]
      });
    });

    var onSuccess = function(url) {
      $scope.$apply(function() {
        $scope.imgs.push(url);
      });
    };
    var onFail = function(message) {
      Loading.tip(message);
    };

    $scope.setPicture = function() {
      $scope.pickModal = $ionicPopup.show({
        template: '<button class="button button-full button-balanced" ng-click="pickFromGallery()">从相册选择</button><button class="button button-full button-positive" ng-click="pickFromCamera()">拍照</button>',
        scope: $scope,
        buttons: [{
          text: '关闭'
        }]
      });
    };
    $scope.removePicture = function(i) {
      $scope.removeModal = $ionicPopup.show({
        template: '是否要移除该图片',
        scope: $scope,
        buttons: [{
          text: '是',
          type: 'button-balanced',
          onTap: function(e) {
            $scope.imgs.splice(i, 1);
            $scope.removeModal.close();
          }
        }, {
          text: '否'
        }]
      });
    };

    $scope.pickFromGallery = function() {
      if (navigator.camera) {
        navigator.camera.getPicture(onSuccess, onFail, {
          destinationType: Camera.DestinationType.DATA_URL,
          sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
          encodingType: Camera.EncodingType.JPEG,
          quantity: 50,
        });
      }
      $scope.pickModal.close();
    };
    $scope.pickFromCamera = function() {
      if (navigator.camera) {
        navigator.camera.getPicture(onSuccess, onFail, {
          destinationType: Camera.DestinationType.DATA_URL,
          sourceType: Camera.PictureSourceType.CAMERA,
          encodingType: Camera.EncodingType.JPEG,
          quantity: 50,
        });
      }
      $scope.pickModal.close();
    };
    $scope.postNewTopic = function() {
      if (!$scope.content && $scope.imgs.length === 0) {
        return Loading.tip('请输入文字或图片');
      }

      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .post(config.domain + '/mobile/add_circle_topic', {
            uid: user.id,
            content: $scope.content,
            imgs: $scope.imgs
          })
          .success(function(result) {
            Loading.tip('已提交');
            sure_exit = true;
            $scope.$root.$broadcast('postCircle');
            $ionicHistory.goBack();
          })
          .catch(function(error) {

          })
      }
    }
  })
  .controller('NewQuestionCtrl', function($scope, $ionicPopup, $state, $ionicHistory, $ionicScrollDelegate, $timeout, $http, Loading, User) {
    $scope.imgs = [];
    $scope.content = '';
    //$scope.imgs.push('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');

    var onSuccess = function(url) {
      $scope.$apply(function() {
        $scope.imgs.push(url);
      });
    };
    var onFail = function(message) {
      Loading.tip(message);
    };

    $scope.setPicture = function() {
      $scope.pickModal = $ionicPopup.show({
        template: '<button class="button button-full button-balanced" ng-click="pickFromGallery()">从相册选择</button><button class="button button-full button-positive" ng-click="pickFromCamera()">拍照</button>',
        scope: $scope,
        buttons: [{
          text: '关闭'
        }]
      });
    };
    $scope.removePicture = function(i) {
      $scope.removeModal = $ionicPopup.show({
        template: '是否要移除该图片',
        scope: $scope,
        buttons: [{
          text: '是',
          type: 'button-balanced',
          onTap: function(e) {
            $scope.imgs.splice(i, 1);
            $scope.removeModal.close();
          }
        }, {
          text: '否'
        }]
      });
    };

    $scope.pickFromGallery = function() {
      if (navigator.camera) {
        navigator.camera.getPicture(onSuccess, onFail, {
          destinationType: Camera.DestinationType.DATA_URL,
          sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
          encodingType: Camera.EncodingType.JPEG,
          quantity: 50,
        });
      }
      $scope.pickModal.close();
    };
    $scope.pickFromCamera = function() {
      if (navigator.camera) {
        navigator.camera.getPicture(onSuccess, onFail, {
          destinationType: Camera.DestinationType.DATA_URL,
          sourceType: Camera.PictureSourceType.CAMERA,
          encodingType: Camera.EncodingType.JPEG,
          quantity: 50,
        });
      }
      $scope.pickModal.close();
    };
    $scope.postNewQuestion = function() {
      if (!$scope.content && $scope.imgs.length === 0) {
        return Loading.tip('请输入文字或图片');
      }

      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .post(config.domain + '/mobile/add_question', {
            uid: user.id,
            title: '',
            content: $scope.content,
            imgs: $scope.imgs
          })
          .success(function(result) {
            Loading.tip('已提交');
            $scope.$root.$broadcast('addQuestion');
            $ionicHistory.goBack();
          })
          .catch(function(error) {

          })
      }
    }
  })
  .controller('ServicesCtrl', function($scope, $state) {
    $scope.services = [{
      id: 1,
      name: '洗车',
      price: 20,
      description: '专业洗车30年',
      distance: '1',
      cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
    }, {
      id: 2,
      name: '洗洗车',
      price: 30,
      description: '专业洗车30年',
      distance: '1.5',
      cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
    }, {
      id: 3,
      name: '一般洗车',
      price: 50,
      description: '专业洗车30年',
      distance: '2',
      cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
    }, {
      id: 4,
      name: '非常洗车',
      price: 60,
      description: '专业洗车30年',
      distance: '5',
      cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
    }];

    $scope.showDetail = function() {
      $state.go('product', {
        id: 0
      });
    };
  })
  .controller('ServicesCategoryCtrl', function($scope, $state) {
    $scope.showCategory = function(name) {
      $state.go('categories', {
        keyword: name
      });
    };
    $scope.choose = function(tab) {
      $scope.choice = tab;
      if (tab === 1) {
        $scope.services = [{
          name: '洗车'
        }, {
          name: '镀膜'
        }, {
          name: '镀晶'
        }, {
          name: '打蜡'
        }, {
          name: '贴膜'
        }, {
          name: '底盘装甲'
        }, {
          name: '内饰清洗'
        }, {
          name: '空调清洗'
        }, {
          name: '钣金喷漆'
        }];
      }

      if (tab === 2) {
        $scope.services = [{
          name: '四轮定位'
        }, {
          name: '车辆检测'
        }, {
          name: '保养套餐'
        }, {
          name: '换空气滤'
        }, {
          name: '换空调滤'
        }, {
          name: '更换汽油滤'
        }, {
          name: '换火花塞'
        }, {
          name: '换蓄电池'
        }, {
          name: '换刹车盘／片'
        }, {
          name: '更换轮胎'
        }, {
          name: '更换防冻液'
        }, {
          name: '更换正时皮带'
        }, {
          name: '更换灯泡'
        }, {
          name: '换机油机滤'
        }];
      }

      if (tab === 3) {
        $scope.services = [{
          name: '安装摄像头'
        }, {
          name: '装导航'
        }, {
          name: '装倒车影像'
        }, {
          name: '装倒车雷达'
        }];
      }
    };
    $scope.showService = function() {
      $state.go('services');
    };
    $scope.choose(1);
    $scope.choice = 1;

  })
  .controller('RegionsCtrl', function($scope, $state, $http, $ionicHistory, $q, Loading, User, Location) {
    var fetchRegions = function() {
      var deferred = $q.defer();
      $http
        .get(config.domain + '/mobile/select_city')
        .success(function(result) {
          $scope.regions = result;
          deferred.resolve();
        })
        .error(function() {
          deferred.resolve();
        });

      return deferred.promise;
    };

    var getLocation = function() {
      var deferred = $q.defer();
      $scope.progress = '正在定位';
      Location
        .current()
        .then(function(result) {
          $scope.location = result;
          deferred.resolve();
        })
        .then(null, function() {
          $scope.process = '定位时发生错误';
          deferred.resolve();
        });

      return deferred.promise;
    };

    $scope.confirmCurrentLocation = function(id) {
      var city = _.find($scope.regions, function(region) {
        return region.id === id;
      });
      User.setCity(city);
      $ionicHistory.goBack();
    };

    fetchRegions()
      .then(getLocation)
      .then(function() {
        if ($scope.location) {
          var id = null;
          _.each($scope.regions, function(region) {
            if (region.name === $scope.location.address.city) {
              id = region.id;
            }
          });

          if (id) {
            $scope.location.id = id;
            $scope.progress = null;
          } else {
            $scope.progress = '您所在的区域不支持服务';
          }
        } else {
          $scope.progress = '没有获取到您的位置';
        }
      })
      .then(null, function() {
        $scope.progress = '无法获取您的位置';
      });
  })
  /*产品详情页control*/
  .controller('ProductCtrl', function($scope, $timeout, $http, $resource, $state, $window, $location, $ionicPopup, $ionicScrollDelegate, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {
    var refreshProduct = function() {
      Loading.show();
      $http
        .get(config.domain + '/mobile/product/' + $state.params.id)
        .success(function(product) {
          Loading.close();
          product.pics = _.map(product.pics, function(item) {
            item.img = config.domain + item.img;
            return item;
          });
          $scope.product = product;
          $scope.product.limit = product.xgperusernum || 0;
          $scope.product.renaming = product.xgtotalnum || 0;
          $scope.favorite = Favorite.containsProduct(product.psid);
          $scope.standards = product.standards;
          $scope.hasMore = true;
          $scope.setStandard(product.psid);
          $ionicSlideBoxDelegate.update();
        });
    };
    var refreshStore = function() {
      $scope.store = {
        id: 1,
        name: '车之翼专业车维护'
      };
    };

    $scope.cancelFavorite = function(id) {
      var userId = null,
        user = User.current();

      if (user) {
        userId = user.id;
      }

      Favorite.removeProduct(userId, id);
      Loading.tip('已取消收藏', 1000);
    };

    $scope.doFavorite = function(id) {
      if ($scope.favorite) {
        $scope.cancelFavorite(id);
      } else {
        $scope.favoriteProduct(id);
      }

      $scope.favorite = !$scope.favorite;

    };

    $scope.favoriteProduct = function(id) {
      var userId = null,
        user = User.current();

      if (user) {
        userId = user.id;
      }

      Favorite.favoriteProduct(userId, id);
      Loading.tip('已收藏', 1000);
    };

    $scope.buy = function() {
      var user = User.current();
      ShopCar.put($scope.product);
      Loading.tip('已加入到购物车', 1000);

      if (user) {
        ShopCar.upload(user.id, ShopCar.all());
      }
    };


    $scope.ordernow = function() {
      var user = User.current();
      ShopCar.put($scope.product);
      $state.go('shopcar');
      $timeout(function() {
        $scope.$root.$broadcast('tab:changeToCart');
      }, 1000);

      if (user) {
        ShopCar.upload(user.id, ShopCar.all());
      }
    };

    $scope.addQuantity = function(num) {
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
      $scope.quantity = quantity;
    };

    $scope.showDetail = function() {
      $state.go('product-detail', {
        id: $scope.product.psid
      });
    };

    $scope.setStandard = function(psid) {
      $scope.chooseStandard = _.find($scope.standards, function(standard) {
        return standard.psid === parseInt(psid);
      });
    };

    $scope.showComments = function(psid) {
      $state.go($state.$current.name + '-comments', {
        psid: $scope.product.psid
      });
    };

    $scope.share = function(psid) {
      var title = $scope.product.name + '只需' + $scope.product.price + ' 元,只在车装甲',
        url = 'http://www.520czj.com/product/' + psid;

      $window.plugins.socialsharing.share(title, null, null, url);
    };

    $scope.showStore = function(id) {
      $state.go('store', {
        id: id
      });
    };

    $scope.quantity = 1;
    $scope.hasMore = false;
    refreshProduct();

    var index = 1,
      size = 20,
      user = User.current(),
      userID = null;

    if (user) {
      userID = user.id;
    }

    $scope.fetchComments = function() {
      $scope.hasMore = false;

      $http
        .get(config.domain + '/mobile/comment/list', {
          params: {
            userId: userID,
            size: size,
            index: index,
            psid: $scope.product.psid
          }
        })
        .success(function(result) {
          if (result) {
            if (result.items && result.items.length > 0) {
              index++;

              if ($scope.comments) {
                result.items = _.union(result.items, $scope.comments.items);
              }

              $scope.hasMore = true;
              $scope.comments = result;
              $ionicScrollDelegate.resize();
            }
          }

          $scope.$broadcast('scroll.infiniteScrollComplete');
        })
        .catch(function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
        });
    };
  })
  /*
   线下商品详情路由
   */
  .controller('StoreCtrl', function($scope, $ionicSlideBoxDelegate, $http, $state, $window, $location, Favorite, User, Loading) {
    $scope.show = function() {
      Loading.show();
      $http
        .get(config.domain + '/mobile/store/' + $state.params.id)
        .success(function(result) {
          $scope.store = result;
          $scope.store.pics = _.map($scope.store.pics, function(item) {
            item.img = config.domain + item.img;
            return item;
          });
          $scope.favorite = Favorite.containsStore(result.id);

          $ionicSlideBoxDelegate.update();
          Loading.close();
        });
    };
    $scope.doFavorite = function(storeID) {
      var userID = null;
      var user = User.current();
      if (user) {
        userID = user.id;
      }

      if ($scope.favorite) {
        Favorite.removeStore(userID, storeID);
      } else {
        Favorite.favoriteStore(userID, storeID);
      }

      $scope.favorite = !$scope.favorite;

    };
    $scope.showProducts = function(code) {
      ///categories/:storeID/:locateCategoryCode/:keyword/:type
      $state.go('categories', {
        storeID: $scope.store.id
      });
    };
    $scope.navigate = function(storeID) {
      $state.go('navigate', {
        x: $scope.store.x,
        y: $scope.store.y
      });
    };
    $scope.showAllService = function() {
      $scope.isShowAllService = true;
    };
    $scope.showAllCommodity = function() {
      $scope.isShowAllCommodity = true;
    };
    $scope.isShowAllService = false;
    $scope.isShowAllCommodity = false;
    $scope.show();
  })
  .controller('ProductsCtrl', function($scope, $http, $state, $window, $location, User, Loading) {
    var refreshCategory = function() {
        $scope.categories = [{
          code: '00',
          name: '免费'
        }, {
          code: '01',
          name: '特价'
        }, {
          code: '02',
          name: '润滑油'
        }, {
          code: '03',
          name: '轮胎'
        }, {
          code: '04',
          name: '保养'
        }];
        //refreshProducts($state.params.code || '');
        $scope.switch($state.params.code || 'all');
        return;
        Loading.show();

        $http
          .get(config.domain + '/store/' + $state.params.store)
          .then(function(result) {
            $scope.categories = result;
            Loading.close();
            refreshProducts($state.params.code || '');
          });
      },
      refreshProducts = function(code) {
        if (!$scope.categories) {
          return;
        }
        $scope.products = [{
          id: 1,
          name: '洗车',
          price: 20,
          description: '专业洗车30年',
          cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
        }, {
          id: 2,
          name: '洗洗车',
          price: 30,
          description: '专业洗车30年',
          cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
        }, {
          id: 3,
          name: '一般洗车',
          price: 50,
          description: '专业洗车30年',
          cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
        }, {
          id: 4,
          name: '非常洗车',
          price: 60,
          description: '专业洗车30年',
          cover: 'http://p1.meituan.net/deal/227af9a7c88fbc02add1b47fd1c38d55260904.jpg'
        }];

        return;
        Loading.show();

        $http
          .get(config.domain + '/store/products/' + code)
          .then(function(result) {
            $scope.products = result;
            Loading.close();
          });
      };

    $scope.switch = function(code) {
      if ($scope.choose == code) {
        return;
      }

      $scope.choose = code;
      refreshProducts(code);
    };

    $scope.showProductDetail = function(id) {
      $state.go('product', {
        store: $state.params.store,
        id: id
      });
    };

    refreshCategory('all');
  })
  .controller('StoreProductCtrl', function($scope, $resource, $state, $window, $location, $ionicPopup, $ionicScrollDelegate, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {

    var storeID = $state.params.storeID || localStorage.storeID,
      fetchProduct = function() {
        var resources = $resource(config.domain + '/mobile/store_product/' + $state.params.id + '?sid=' + storeID),
          user = User.current();

        Loading.show();
        resources.get(
          function(product) {
            if (product.status === 1) {
              Loading.close();
              product.pics = _.map(product.pics, function(item) {
                item.img = config.domain + '/upload/' + product.sku + '/' + item.img;
                return item;
              });
              $scope.product = product;
              $scope.favorite = Favorite.containsProduct(product.psid);
              $ionicSlideBoxDelegate.update();
            } else {
              $ionicHistory.goBack();
              Loading.tip('抱歉,该商品暂时不可用或已下架');
            }
          },
          function(data) {
            Loading.tip('应用异常');
            console.log(data);
          });
      };

    $scope.closeCopies = function() {
      $scope.status = 'SUMMARY';
      $ionicScrollDelegate.scrollTop();
    };
    $scope.buy = function() {
      var user = User.current(),
        checked = _.where($scope.copies, {
          checked: true
        }),
        checkQuantityResource = $resource(config.domain + '/mobile/check_cart'),
        counter = 0,
        hasError = false,
        successCount = 0,
        all = checked.length,
        onFinish = function() {
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
        _.each(checked, function(copie) {
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
          }, function(result) {
            if (result && result.flag === 1) {
              ShopCar.put(newProduct);
              successCount++;
            } else {
              hasError = true;
            }

            copie.error = result.msg;
            copie.checked = false;

            onFinish();
          }, function(error) {
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
    $scope.showCopies = function() {

      $scope.status = 'DETAIL';
      $ionicScrollDelegate.resize();
    };
    $scope.showDetail = function() {
      $state.go('detail', {
        id: $scope.product.psid
      });
    };
    $scope.chooseCopie = function(id) {
      var exists = _.find($scope.copies, function(copie) {
        return copie.poid === parseInt(id);
      });

      if (exists) {
        exists.checked = !exists.checked;
        exists.error = '';
        $scope.resumeWithCopies();
      }
    };
    $scope.resumeWithCopies = function() {
      var checked = _.where($scope.copies, {
        checked: true
      });
      var resume = 0;
      _.each(checked, function(item) {
        resume += item.price;
      });

      $scope.resumeForCopies = parseFloat(resume.toFixed(2));
      $scope.chooseCopies = checked.length;
    };
    $scope.showComments = function(psid) {
      $state.go($state.$current.name + '-comments', {
        psid: $scope.product.psid
      });
    };
    $scope.share = function(psid) {
      // var title = '新鲜' + $scope.product.name + '只需' + $scope.product.price + ' 元,只在易凡网',
      //   url = 'http://www.eofan.com/product/' + psid;

      $window.plugins.socialsharing.share(title, null, null, url);
    };
    $scope.chooseCopies = 0;
    $scope.status = 'SUMMARY';

    fetchProduct();
  })
  /*产品图片详情页control*/
  .controller('PDetailCtrl', function($scope, $resource, $state, Loading) {
    var productHelper = $resource(config.domain + '/mobile/pdetail/' + $state.params.id);
    Loading.show();
    productHelper.query(
      function(pics) {

        Loading.close();
        $scope.pics = _.map(pics, function(item) {
          item.img = config.domain + '/upload/' + item.img;
          return item;
        });
      },
      function(data) {
        Loading.close();
        Loading.tip('应用异常');
        console.log(data)
      });
  })
  /*
   *分类查找产品control
   */
  .controller('CategoriesCtrl', function($scope, $ionicModal, $http, $resource, $state, $q, $ionicScrollDelegate, $ionicSideMenuDelegate, $location, $timeout, SearchKeywords, Loading) {
    $scope.chooseCategory = null;
    $scope.owner = 1;
    var index = 1;
    if ($state.params.storeID && $state.params.storeID !== 1) {
      $scope.owner = 0;
    }
    $scope.salesOrderby = '';
    $scope.priceOrderby = '';
    $scope.storeID = $state.params.storeID;
    $scope.keyword = $state.params.keyword || '';
    var fetchCategory = function() {
      var deferred = $q.defer();
      Loading.show();
      $http
        .get(config.domain + '/mobile/category', {
          params: {
            sid: $scope.storeID
          }
        })
        .success(function(result) {
          var chooseCategory = {
            name: '全部分类',
            code: ''
          };

          if (result && result.length > 0) {
            $scope.categories = _.map(result, function(item) {
              return _.extend(item, {
                id: item.code.replace(/\'/g, '')
              });
            });

            if ($state.params.locateCategoryCode) {
              chooseCategory = _.find($scope.categories, function(cateogry) {
                return category.code === $state.params.locateCategoryCode;
              });
            }
          }

          $scope.chooseCategory = chooseCategory;
          deferred.resolve();
          Loading.close();
        })
        .catch(function() {
          deferred.resolve();
          Loading.close();
        })

      return deferred.promise;
    };
    var index = 1;
    var fetchProducts = function() {
      var deferred = $q.defer();
      SearchKeywords.add($scope.keyword);
      $scope.hasMore = false;
      if ($scope.chooseCategory) {
        $http
          .get(config.domain + '/mobile/products', {
            params: {
              code: $scope.chooseCategory.id,
              sales: $scope.salesOrderby,
              price: $scope.priceOrderby,
              zy: $scope.owner,
              sid: $scope.storeID,
              keyword: $scope.keyword,
              type: $state.params.type,
              index: index++
            }
          })
          .success(function(result) {
            var newly = _.map(result, function(item) {
              item.cover = config.domain + item.cover;
              return item;
            });

            $scope.products = _.union($scope.products, newly);

            if (newly.length > 0) {
              $scope.hasMore = true;
            }
            deferred.resolve();
          })
          .catch(function() {
            deferred.resolve();
          });
      } else {
        deferred.resolve();
      }

      return deferred.promise;
    };

    $ionicModal
      .fromTemplateUrl('templates/category-modal.html', {
        scope: $scope
      })
      .then(function(modal) {
        $scope.categoryModal = modal;
      });
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };

    $scope.$on('requireChangeCategory', function(event, args) {
      var chooseCategory = _.find($scope.categories, function(category) {
        return category.code == "'" + args.code + "'";
      });

      if (chooseCategory) {
        $scope.chooseCategory = chooseCategory;
        $scope.hasMore = true;
        index = 1;
        $scope.products = [];
        $scope.fetchProducts();
      }
    });

    $scope.changeCategory = function() {
      $scope.categoryModal.show();
    };
    $scope.setAllArea = function(name, code, id) {
        $scope.setCategory(name, code, id);
      },
      $scope.setCategory = function(name, code, id) {
        $scope.chooseCategory = {
          name: name,
          code: code,
          id: id
        };
        $scope.categoryModal.hide();

        $scope.hasMore = true;
        index = 1;
        $scope.products = [];
        fetchProducts();
      };
    $scope.closeServicesModal = function() {
      $scope.categoryModal.hide();
    };
    $scope.changeCateogryOwner = function() {
      if ($scope.owner === 1) {
        $scope.owner = 0;
      } else {
        $scope.owner = 1;
      }
      $scope.hasMore = true;
      index = 1;
      $scope.products = [];
      fetchProducts();
    };
    $scope.setSalesOrderby = function(tag) {
      switch ($scope.salesOrderby) {
        case 'desc':
          $scope.salesOrderby = 'asc';
          break;

        default:
          $scope.salesOrderby = 'desc';
      }

      $scope.hasMore = true;
      index = 1;
      fetchProducts();
    };
    $scope.setPriceOrderby = function(tag) {
      switch ($scope.priceOrderby) {
        case 'asc':
          $scope.priceOrderby = 'desc';
          break;

        default:
          $scope.priceOrderby = 'asc';
      }

      $scope.hasMore = true;
      index = 1;
      $scope.products = [];
      fetchProducts();
    };

    fetchCategory()
      .then(fetchProducts);

    $scope.hasMore = false;
    $scope.fetchProducts = fetchProducts;
  })

.controller('HistoryCtrl', function($scope, $ionicModal, $http, $resource, $state, $q, $ionicScrollDelegate, $ionicSideMenuDelegate, $location, $timeout, SearchKeywords, Loading, User) {
    var fetchHistory = function() {
      var user = User.current();
      if (user) {
        $http
          .get(config.domain + '/mobile/get_browse/' + user.id)
          .success(function(result) {
            if (result) {
              $scope.products = _.map(result, function(item) {
                item.cover = config.domain + item.cover;
                return item;
              });
            }
          })
          .catch(function(error) {

          });
      } else {
        $scope.$emit('user:requireLogin');
      }
    };

    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };

    fetchHistory();
  })
  /*
   * 查找control
   */
  .controller('SearchCtrl', function($scope, $state, $resource, Loading, SearchKeywords) {
    var colors = ['balanced', 'calm', 'energized', 'royal'];
    var getRandomColor = function() {
      return colors[_.random(0, 3)];
    };

    $scope.keyword = '';
    $scope.searchProduct = function() {
      if ($scope.keyword.length > 0) {
        //SearchKeywords.add($scope.keyword);
        $state.go('categories', {
          keyword: $scope.keyword
        });
        ///categories/:storeID/:locateCategoryCode/:keyword
      } else {
        Loading.tip('请输入搜索关键词', 1000);
      }
    };

    $scope.setKeyword = function(keyword) {
      $scope.keyword = keyword;

      $scope.searchProduct();
    };
    $scope.removeKeyword = function(keyword) {
      //$scope.keyword = keyword;
      SearchKeywords.remove(keyword);
      $scope.keywords = SearchKeywords.local();
    };
    $scope.clearLocalKeyword = function() {
      SearchKeywords.clearLocalKeyword();
      $scope.keywords = SearchKeywords.local();
    };

    $scope.keywords = SearchKeywords.local();
    $scope.hots = SearchKeywords.hots();
    $scope.hots = _.map($scope.hots, function(hot) {
      hot.css = 'button-' + getRandomColor();
      return hot;
    });
  })
  /*用户中心control*/
  .controller('AccountCtrl', function($scope, $state, $resource, $http, $ionicPopup, $base64, Loading, User) {
    $scope.checkin = function() {
      $scope.CHECKSTATUS = 'CHECKING';
      $http
        .post(config.domain + '/mobile/checkin', {
          userid: User.current().id
        })
        .success(function(result) {
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
        .error(function(error) {
          $scope.CHECKSTATUS = 'UNCHECKED';
          console.log(error);
          Loading.tip('网络或服务器异常');
        });
    };
    $scope.logout = function() {
      var confirmPopup = $ionicPopup.confirm({
        title: '您确定要退出吗？',
        cancelText: '取消',
        okText: '确定'
      });

      confirmPopup.then(function(res) {
        if (res) {
          User.logout();
          $scope.$root.loginModalStatus = 'LOGIN';
          $scope.$root.resetPasswordModel = {};
          $scope.$root.loginModel = {};
          $scope.$root.registerModel = {};
        }
      });
    };
    $scope.buyWithPhone = function() {
      $ionicPopup.confirm({
        title: '通过在线支付方式购买更优惠，您确定继续拨打400电话进行订购吗？',
        cancelText: '取消',
        okText: '继续拨打'
      }).then(function(res) {
        if (res) {
          window.open('tel:4009676558', '_self');
        }
      });
    };
    $scope.resetPassword = function() {
      var user = User.current();
      $scope.$root.resetPasswordModel.userName = user.mobile;
      $scope.$root.loginModalStatus = 'RECOVERPASSWORD';
      $scope.$root.recoveryPasswordOnly = true;
      $scope.$root.loginModal.show();

    };
    $scope.$on('loginSuccess', function(event, args) {
      $scope.user = User.current();
      //if ($scope.user.hascheckedin && $scope.user.hascheckedin > 0) {
      //  $scope.CHECKSTATUS = 'CHECKED';
      //  $scope.checkDays = $scope.user.hascheckedin;
      //} else {
      //  $scope.CHECKSTATUS = 'UNCHECKED';
      //}
    });
    $scope.$on('registSuccess', function(event, args) {
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
    $scope.invite = function() {
      $state.go('tab.invite');
    };
    $scope.$on('$ionicView.afterEnter', function() {
      var user = User.current();
      var resource = $resource(config.domain + '/mobile/payinfo');

      resource.get({
          userid: user.id,
          price: -1
        },
        function(result) {
          if (result.hascheckedin && result.hascheckedin > 0) {
            $scope.CHECKSTATUS = 'CHECKED';
            $scope.checkDays = result.hascheckedin;
          } else {
            $scope.CHECKSTATUS = 'UNCHECKED';
          }
        },
        function(error) {
          console.log(error);
        });
    });

    //if ($scope.user.hascheckedin && $scope.user.hascheckedin > 0) {
    //  $scope.CHECKSTATUS = 'CHECKED';
    //  $scope.checkDays = $scope.user.hascheckedin;
    //} else {
    //  $scope.CHECKSTATUS = 'UNCHECKED';
    //}
  })
  /*重置密码路由*/
  .controller('ResetPassword', function($scope, $state, $http, $ionicHistory, Loading, User) {
    // $scope.WithRegister
    var user = User.current();
    $scope.save = function() {
      if ($scope.newPassword !== $scope.confirmPassword) {
        return Loading.tip('两次密码不一致, 请重新输入');
      }

      Loading.show();

      User
        .resetPassword($scope.mobile, $scope.newPassword)
        .success(function(result) {
          Loading.tip('密码已修改');
        })
        .error(function(error) {
          console.log(error);
          Loading.tip(error.message);
        });
    };

    $scope.newPassword = $scope.mobile = '';
  })
  /*绑定手机路由*/
  .controller('BindMobileCtrl', function($scope, $state, $http, Loading, User) {
    // $scope.WithRegister
    $scope.requestValidateCode = function() {
      $scope.requestCodeProcessing = true;
      User
        .requestValidationCodeModify()
        .then(function(result) {
          $scope.counterWithRequestCode = 60;

          var loop = function() {
            if (--$scope.counterWithRequestCode <= 0) {
              $scope.counterWithRequestCode = 60;
              $scope.requestCodeProcessing = false;
            } else {
              $timeout(loop, 1000);
            }
          };

          loop();
        })
        .catch(function(error) {
          $scope.requestCodeProcessing = false;
          Loading.tip(error.message);
        });
    };

    $scope.save = function() {
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
        .then(function(result) {
          if (result && result.flag == 1) {
            return $state.go('tab.reset-password');
          } else {
            Loading.tip(result.msg);
          }
        })
        .catch(function(error) {
          console.log(error);
          Loading.tip('网络或服务器异常');
        });
    };

    $scope.validationCode = $scope.mobile = '';
  })
  /*我的订单control*/
  .controller('OrderCtrl', function($scope, $state, $resource, $ionicScrollDelegate, User, MyOrders, Loading) {
    var query = function(type) {
      hasMore = false;

      MyOrders
        .query(User.current().id, $scope.index, $scope.size, type).$promise
        .then(function(result) {
          $scope.count = result.items.length;
          $scope.total = result.total;
          if (result && result.items.length > 0) {
            $scope.orders = _.union($scope.orders, result.items);
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

              case 'success':
                $scope.hasMore = _.where(result.items, {
                  status: '未使用'
                }).length > 0;
                break;
            }
            $scope.hasMore = true;
            $ionicScrollDelegate.resize();
            $scope.$broadcast('scroll.infiniteScrollComplete');
          } else {
            $scope.hasMore = false;
            $scope.total = 0;
          }
        }, function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          $scope.hasMore = false;
          console.log(error);
        });
    };

    $scope.load = function() {
      query($scope.choose || 'all', $scope.index || 'indexOfAll');
    };
    $scope.switch = function(choose) {
      $scope.hasMore = true;
      $scope.orders = [];
      $scope.choose = choose;
      $scope.index = 1;
      $scope.hasMore = true;
      $ionicScrollDelegate.scrollTop();
    };

    $scope.showDetail = function(oid, status) {
      $state.go('order-detail', {
        id: oid
      });
    };
    $scope.$root.$on('cancelOrder', function(event, args) {
      var exists = _.filter($scope.orders, function(order) {
        return order.id == args.id;
      });

      if (exists && exists.length > 0) {
        var exist = exists[0];
        exist.status = '已取消';
      }
    });
    $scope.$root.$on('order:fetchSuccess', function(event, args) {
      if (args.order) {
        $scope.orders = _.map($scope.orders, function(order) {
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
  .controller('ContinuePayCtrl', function($scope, $state, $resource, $http, $q, $ionicHistory, $filter, $ionicPopup, AliPay, User, Loading) {
    var id = $state.params.id,
      alipayFinishCallback = function(args) {
        Loading.show(1);
        $http
          .get(config.domain + '/mobile/order/status?orderid=' + args.ono)
          .success(function(result) {
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
          .catch(function(error) {
            Loading.tip('网络或服务器出现错误');
            $ionicHistory.goBack();
            //$state.go('tab.order');
            //$ionicHistory.clearHistory();
          });
      },
      checkTimeRange = function() {
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
      location = function() {
        var deferred = $q.defer(),
          user = User.current();

        $http
          .get(config.domain + '/map/getMinDistanceStore', {
            params: {
              address: ($scope.order.take_address || '').replace(/ /g, '')
            }
          })
          .success(function(result) {
            if (result && result.flag === 1) {
              $scope.hiddenTimeRegion = false;
              $scope.timeRange = checkTimeRange();
            } else {
              $scope.hiddenTimeRegion = true;
            }

            deferred.resolve();
          })
          .catch(function(error) {
            console.log(error);
            deferred.resolve();
          });

        return deferred.promise;
      },
      fetchOrder = function(id) {
        var deferred = $q.defer();

        $http
          .get(config.domain + '/mobile/orderdetail', {
            params: {
              id: id
            }
          })
          .success(function(result) {
            $scope.order = result;
            $scope.order.deliverynum = $scope.order.deliverynum || "";
            $scope.order.paymentValue = $scope.order.paymentValue + '';
            resume();
            deferred.resolve();
          })
          .catch(function(error) {
            console.log(error);
            Loading.tip("应用或服务器异常");
            deferred.reject(error);
          });

        return deferred.promise;
      },
      updateProfile = function() {
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
            .success(function(result) {
              $scope.balance = user.balance = result.balance;
              deferred.resolve();
            })
            .catch(function(error) {
              $scope.balance = 0;
              deferred.resolve();
            });

        } else {
          $scope.balance = 0;
          deferred.resolve();
        }

        return deferred.promise;
      },
      resume = function() {
        var renaminprice = $scope.order.currentprice || 0;

        if ($scope.balanceUsed > 0) {
          renaminprice -= $scope.balance;
        }

        $scope.renaminprice = renaminprice;

      },
      load = function() {
        $scope.balanceUsed = 0;
        Loading.show();

        fetchOrder(id)
          .then(location)
          .then(updateProfile)
          .then(function() {
            Loading.close();
          })
          .catch(function(error) {
            Loading.tip('应用异常');
            $ionicHistory.goBack();
          });
      };

    $scope.pay = function() {};
    $scope.useBalance = function() {
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
    $scope.$root.$on('pay-balance', function(event, args) {
      $scope.balanceUsed = parseFloat(args.use.toFixed(2));
      $scope.payUseBalance = true;
      resume();
    });
    $scope.$root.$on('cancel-balance', function(event, args) {
      $scope.balanceUsed = 0;
      $scope.payUseBalance = false;
      resume();
    });

    load();
  })
  /*订单详情control*/
  .controller('OrderDetailCtrl', function($scope, $state, $resource, $http, $ionicPopup, $ionicHistory, AliPay, MyOrders, Loading) {
    var id = $state.params.id,
      fetchOrder = function(id) {
        Loading.show();
        orderHelper.get({
            id: id
          },
          function(data) {
            Loading.close();
            $scope.order = data;
            $scope.$root.$broadcast('order:fetchSuccess', {
              order: data
            });

            fetchExpress(data.deliverynum);
          },
          function(data) {
            Loading.tip('应用异常');
            console.log(data);
          });
      },
      fetchExpress = function(devilyNumber) {
        $http.get('http://www.kuaidi100.com/query?type=zhaijisong&postid=' + devilyNumber)
          .success(function(result) {
            if (result && result.status == '200') {
              return $scope.expresses = result.data;
            }

            $scope.expressProgress = '正在处理';
            console.log(result);
          })
          .error(function(result) {
            $scope.expressProgress = '查询异常,请稍后再试';
          });
      },
      orderHelper = $resource(config.domain + '/mobile/orderdetail'),
      alipayFinishCallback = function(args) {
        Loading.show(1);
        $http
          .get(config.domain + '/mobile/order/status?orderid=' + args.ono)
          .success(function(result) {
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
          .catch(function(error) {
            Loading.tip('网络或服务器出现错误');
            $ionicHistory.goBack();
          });
      };


    $scope.expressProgress = '正在查询, 请稍后';
    $scope.status = status;
    $scope.paying = false;
    $scope.continuePay = function() {
      $state.go('continue-pay', {
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
        function(result) {
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
        function(error) {
          Loading.tip('支付失败，请稍后再试');
          console.log(error);
          $scope.paying = false;
        }
      );
    };
    $scope.cancelOrder = function() {
      var resource = $resource(config.domain + '/mobile/user/order/changestatus');
      if ($scope.order.status !== '待付款' && ($scope.order.paymentValue == '1' || $scope.order.paymentValue == '3')) {

        $ionicPopup.show({
          title: '退款说明',
          template: '<p class="grey">账户余额可立即到账, 原路返回支付宝需要5-7个工作日</p>',
          buttons: [{
            text: '原路返回',
            onTap: function() {
              Loading.show();
              resource = $resource(config.domain + '/mobile/user/order/changestatus');
              resource.save({
                status: 5,
                id: $state.params.id,
                refund: 0
              }, function(result) {
                if (result.err == 1) {
                  return Loading.tip(result.msg);
                }

                Loading.close();
                $scope.$root.$broadcast('cancelOrder', {
                  id: $state.params.id
                });
                $ionicHistory.goBack();
              }, function(error) {
                Loading.tip('应用异常');
                console.log(error);
              });
            }
          }, {
            text: '账户余额',
            type: 'button-assertive',
            onTap: function() {
              Loading.show();
              resource = $resource(config.domain + '/mobile/user/order/changestatus');
              resource.save({
                status: 5,
                id: $state.params.id,
                refund: 1
              }, function(result) {
                if (result.err == 1) {
                  return Loading.tip(result.msg);
                }

                Loading.close();
                $scope.$root.$broadcast('cancelOrder', {
                  id: $state.params.id
                });
                $ionicHistory.goBack();
              }, function(error) {
                Loading.tip('应用异常');
                console.log(error);
              });
            }
          }, {
            text: '取消'
          }]
        });
      } else {
        Loading.show();

        resource = $resource(config.domain + '/mobile/user/order/changestatus');
        resource.save({
          status: 5,
          id: $state.params.id,
          refund: 0
        }, function(result) {
          if (result.err == 1) {
            return Loading.tip(result.msg);
          }

          Loading.close();
          $scope.$root.$broadcast('cancelOrder', {
            id: $state.params.id
          });
          $ionicHistory.goBack();
        }, function(error) {
          Loading.tip('应用异常');
          console.log(error);
        });
      }
    };
    $scope.comment = function(oiid, psid) {
      $state.go('tab.order-comment', {
        oiid: oiid,
        psid: psid
      });
    };
    $scope.$root.$on('comment', function(event, args) {
      var comment = args.comment;

      $scope.order.items = _.map($scope.order.items, function(item) {
        if (item.id == comment.oiid) {
          item.hascomment = 1;
        }

        return item;
      });
    });
    $scope.$on('$ionicView.afterEnter', function() {
      fetchOrder(id);
    });
  })
  /*邀请好友路由*/
  .controller('InviteCtrl', function($scope, $base64, User, Loading) {
    var user = User.current(),
      title = '我发现了一个很方便的果蔬速递网站，质量价格都不错，来试试吧！',
      url = 'http://www.eofan.com/signup?c=' + $base64.encode(user.mobile);

    $scope.share = function() {
      if (window.plugins && window.plugins.socialsharing) {
        window.plugins.socialsharing.share(title + ' ' + url);
      }
    };
    $scope.copy = function() {
      Loading.tip('已复制');
    };
    $scope.content = title + ' ' + url;
  })
  /*购物车Control*/
  .controller('CarCtrl', function($scope, $resource, $filter, $state, $ionicPopup, $http, User, ShopCar, Loading) {
    var resumeShopCarNumber = function() {
      $scope.$root.carNumber = ShopCar.all().length;
    };
    var fetchCarProduct = function() {
      ShopCar
        .fetchProduct()
        .then(function() {
          Loading.close();
          $scope.shopCarItems = ShopCar.all();
        });
    };

    $scope.$watch('shopCarItems', function() {
      $scope.hasCheckItems = _.where($scope.shopCarItems, {
        'checked': true
      }).length > 0;

      $scope.total = ShopCar.resumeTotalPrice($scope.shopCarItems);
    }, true);

    $scope.$root.$on('user:logoutSuccess', function(event, user) {
      $scope.$root.carNumber = 0;
      ShopCar.clear();
    });
    $scope.pay = function(pid, psid) {
      ShopCar.setPayOptionals(_.where($scope.shopCarItems, {
        'checked': true
      }));

      $state.go('pay', {}, {
        reload: true
      });
    };

    $scope.checkAll = function() {
      _.each($scope.cars, function(car) {
        if (car && car.product && car.product.status == '1') {
          car.checked = true;
        }
      });
    };
    $scope.addQuantity = function(id, count) {
      var user = User.current();
      var carItem = _.find($scope.shopCarItems, function(shopCarItem) {
        return shopCarItem.psid === id;
      });

      if (carItem) {
        var quantity = carItem.quantity + count;
        if (quantity < 1) {
          quantity = 1;
        }
        if(quantity > carItem.product.quantity){
                quantity =  carItem.product.quantity;
                Loading.tip('购买数量不能超过库存');
              }

        carItem.quantity = quantity;

        ShopCar.setOptionals($scope.shopCarItems);
        if (user) {
          ShopCar.upload(user.id);
        }
      }
    };
    $scope.clearShopCar = function() {
      var user = User.current(),
        userID = null;
      if (user) {
        userID = user.id;
      }

      $ionicPopup.show({
        title: '询问',
        template: '是否要清除购物车?',
        buttons: [{
          text: '<b >是</b>',
          type: 'button-balanced',
          onTap: function() {
            var userID = null;
            if (User.current()) {
              userID = User.current().id;
            }

            ShopCar.clear(userID);
            $scope.shopCarItems = ShopCar.all();
          }
        }, {
          text: '否'
        }]
      });
    }
    $scope.removeCar = function(id) {
      $ionicPopup.show({
        title: '询问',
        template: '是否要从购物车移除?',
        buttons: [{
          text: '<b >是</b>',
          type: 'button-balanced',
          onTap: function() {
            var userId = null;
            if (User.current()) {
              userId = User.current().id;
            }

            ShopCar.remove(userId, id);
            $scope.shopCarItems = ShopCar.all();
          }
        }, {
          text: '否'
        }]
      });
    };
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };

    $scope.$root.$on('tab:changeToCart', function() {
      Loading.show();

      if ($scope.$root.user) {
        User.updateProfile();
      } else {
        fetchCarProduct();
      }

      resumeShopCarNumber();
    });
    $scope.$root.$on('user:updateProfileSuccess', function() {
      fetchCarProduct();
    });
    $scope.$on('shopCar:addItemSuccess', function() {
      $scope.shopCarItems = ShopCar.all();
    });
    $scope.$on('shopCar:removeItemSuccess', function() {
      $scope.shopCarItems = ShopCar.all();
    });
    $scope.shopCarItems = [];
    resumeShopCarNumber();
  })
  /*
   *支付Control
   */
  .controller('PaymentCtrl', function($scope, $state, $filter, $resource, $timeout, $ionicHistory, $ionicPopup, $ionicScrollDelegate, AliPay, $http, $q, ShopCar, MyAddress, User, Loading) {
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
      profileWithoutAddress = function() {
        var resource = $resource(config.domain + '/mobile/payinfo'),
          deferred = $q.defer();

        resource.get({
            userid: user.id,
            price: order.currentprice
          },
          function(result) {
            user.addresses = result.address;
            user.balance = result.balance;
            discountThreshold = parseFloat(parseFloat(result.discountthreshold || 0).toFixed(2));
            discount = parseFloat(parseFloat(result.discount || 0).toFixed(2));
            freeShippingFee = parseFloat(parseFloat(result.freeshippingfee || 0).toFixed(2));
            shippingFee = parseFloat(parseFloat(result.shippingfee | 0).toFixed(2));
            $scope.freeShippingFee = freeShippingFee;
            deferred.resolve();
          },
          function(error) {
            console.log(error);
            deferred.reject('应用异常，没有获取到支付信息');
          });

        return deferred.promise;
      },
      profile = function() {
        var resource = $resource(config.domain + '/mobile/payinfo'),
          deferred = $q.defer();

        resource.get({
            userid: user.id,
            price: order.currentprice
          },
          function(result) {
            user.addresses = result.address;
            user.balance = result.balance;
            discountThreshold = parseFloat((parseFloat(result.discountthreshold || 0)).toFixed(2));
            discount = parseFloat((parseFloat(result.discount || 0)).toFixed(2));
            freeShippingFee = parseFloat((parseFloat(result.freeshippingfee || 0)).toFixed(2));
            shippingFee = parseFloat((parseFloat(result.shippingfee || 0)).toFixed(2));
            $scope.freeShippingFee = freeShippingFee;
            defaultAddress = MyAddress.getDefaultAddress(user.addresses);
            if (defaultAddress) {
              order.addrid = 0 || defaultAddress.id;
            }
            deferred.resolve();
          },
          function(error) {
            console.log(error);
            deferred.reject('应用异常，没有获取到支付信息');
          });

        return deferred.promise;
      },
      checkProducts = function() {
        var deferred = $q.defer();

        order.payment = '1';
        order.coupon_code = '';
        order.balance = 0;
        order.coupon = 0;
        items = [];

        cars = ShopCar.getPayOptionals();
        _.each(cars, function(car) {
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

        order.items = items;
        order.giftitems = gifts;

        if (cars.length === 0) {
          deferred.reject('emptyProducts');
        } else {
          deferred.resolve();
        }

        return deferred.promise;
      },
      coupons = function() {
        var resource = $resource(config.domain + '/mobile/coupons'),
          deferred = $q.defer(),
          total = order.currentprice;

        if (extra === 'PRESALE') {
          deferred.resolve();
        } else {
          resource.query({
            userid: User.current().id,
            type: 'unuse'
          }, function(result) {
            var coupons = _(result)
              .chain()
              .reject(function(coupon) {
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
          }, function(err) {
            console.log(err);
            deferred.reject('应用异常, 没有自动使用优惠券');
          });
        }

        return deferred.promise;
      },
      location = function() {
        var deferred = $q.defer(),
          defaultAddress = null,
          user = User.current();

        if (user) {
          defaultAddress = MyAddress.getAddressByID(order.addrid, user.addresses);
        }

        deferred.resolve();

        return deferred.promise;
      },
      checkTimeRange = function() {
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
      load = function(total) {
        Loading.show();

        checkProducts()
          .then(profile)
          .then(location)
          .then(resume)
          .then(coupons)
          .then(resume)
          .then(function() {
            Loading.close();
            $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
          })
          .catch(function(error) {

            Loading.close();
            var via = error || '';

            if (via === 'emptyProducts') {
              Loading.tip('没有要支付的商品');
              return $ionicHistory.goBack();
            }

            $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
          });
      },
      resume = function() {
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


        _.each(cars, function(car) {
          price = parseFloat(car.quantity * car.product.price);
          $scope.order.price += parseFloat(price.toFixed(2));
        });

        // $scope.order.price = parseFloat($filter('number')(price, 2));
        // $scope.renaminprice = $scope.order.currentprice = $scope.order.price + shippingFee;
        $scope.renaminprice = parseFloat(($scope.order.price - $scope.order.balance - $scope.order.offPrice + $scope.order.shippingprice).toFixed(2));
        $scope.order.currentprice = parseFloat(($scope.order.price + $scope.order.shippingprice).toFixed(2));
        // parseFloat($filter('number')($scope.order.price - $scope.order.coupon - $scope.order.balance - $scope.order.offPrice + $scope.order.shippingprice, 2));

        // _.each(presales, function(presaleItem) {
        //   price = $filter('number')((presaleItem.quantity * presaleItem.price), 2);
        //   $scope.order.price += parseFloat(price);
        // });
        // $scope.order.price += order.shippingprice;
        // $scope.order.price = parseFloat($filter('number')($scope.order.price, 2));
        //
        // if ($scope.order.price < freeShippingFee) {
        //   $scope.differenceWithShipping = parseFloat($filter('number')(freeShippingFee - $scope.order.price, 2));
        //   $scope.order.shippingprice = shippingFee;
        //   $scope.order.currentprice += shippingFee;
        // }
        //
        // // 计算应支付的金额
        // // 应支付的金额 ＝ 商品价格 ＋ 物流费用 － 优惠券
        // $scope.order.currentprice = 0;
        // $scope.order.currentprice = parseFloat($filter('number')($scope.order.price - $scope.order.coupon + $scope.order.shippingprice, 2));
        // if ($scope.order.currentprice >= discountThreshold) {
        //   $scope.order.currentprice -= discount;
        //   $scope.order.offPrice = discount;
        //
        //   if (discountThreshold != discount != 0) {
        //     $scope.offs.push('全场满' + discountThreshold + '元减' + discount + '元');
        //   }
        // }
        //
        // // 还需支付的金额
        // // 还需支付的金额 = 商品价格 ＋ 物流费用 － 优惠券 － 余额
        // $scope.renaminprice = parseFloat($filter('number')($scope.order.price - $scope.order.coupon - $scope.order.balance - $scope.order.offPrice + $scope.order.shippingprice, 2));

        deferred.resolve();
        return deferred.promise;
      },
      alipayFinishCallback = function(args) {
        Loading.show(1);
        $http
          .get(config.domain + '/mobile/order/status?orderid=' + args.orderid)
          .success(function(result) {
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
          .catch(function(error) {
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

    $scope.expandAddress = function() {
      $scope.showAllAddress = true;
    };
    $scope.collapseAddress = function() {
      $scope.showAllAddress = false;
      var user = User.current();
      _.each(user.addresses, function(address, index) {
        if (address.id == user.defaultAddressID) {
          user.addresses.splice(0, 0, user.addresses.splice(index, 1)[0]);
        }
      });
    };
    $scope.pay = function() {
      // Loading.tip('正在申请接口，敬请期待');
      // $ionicHistory.goBack();
      // return;
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

      Loading.show(1);
      var resource = $resource();
      $http
        .post(config.domain + '/mobile/pay', order)
        .success(function(result) {
          //ShopCar.remove(user.id, cars);
          if (result && result.flag === 2) {
            AliPay.pay(result.url, {
                orderid: result.orderid
              })
              .then(alipayFinishCallback);

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
        .catch(function(error) {
          Loading.tip('网络或服务器出现错误');
          $ionicHistory.goBack();
        });
    };

    $scope.setAddress = function(id) {
      Loading.show();
      $scope.order.addrid = id;
      $scope.showAllAddress = false;

      profileWithoutAddress()
        .then(location)
        .then(resume)
        .then(coupons)
        .then(resume)
        .then(function() {
          Loading.close();
          $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
        })
        .catch(function(error) {
          Loading.close();
          var via = error || '';

          if (via === 'emptyProducts') {
            Loading.tip('没有要支付的商品');
            return $ionicHistory.goBack();
          }

          $ionicScrollDelegate.$getByHandle('paymentScroll').resize();
        });
    };
    $scope.modifyAddress = function(id) {
      $scope.$root.new = false;
      $scope.$root.address = MyAddress.getAddressByID(id, User.current().addresses);
      $state.go($state.$current.name + '-address-edit', {
        id: id
      });
    };
    $scope.newAddress = function(id) {
      $scope.$root.new = true;
      $scope.$root.address = {
        province: '陕西省',
        city: '西安市',
        userid: User.current().id,
        tel: '',
        mobile: ''
      };
      $state.go('address-edit', {
        id: id
      });
    };
    $scope.useBalance = function() {
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
    $scope.useCoupon = function() {
      var balance = $scope.order.balance,
        total = parseFloat($scope.order.price - balance);

      if (total < 0) {
        total = 0;
      }

      $state.go('tab.pay-coupon', {
        total: total
      });
    };
    $scope.showOffPriceDetail = function() {
      $scope.isShowOffPriceDetail = !$scope.isShowOffPriceDetail;
    };
    $scope.removeStoreProduct = function() {
      var productsInStore = $scope.storeProducts || [],
        cars = ShopCar.getPayOptionals(),
        user = User.current();

      _.each(productsInStore, function(product) {
        cars = _.reject(cars, function(item) {
          return item.psid === product.psid;
        });
      });

      ShopCar.setPayOptionals(cars);
      load();
    };

    $scope.$root.$on('address:saveNewSuccess', function(event, args) {
      if (args.address) {
        $scope.setAddress(args.address.id);
      }
    });
    $scope.$root.$on('pay-balance', function(event, data) {
      $scope.order.balance = parseFloat(parseFloat($data.use).toFixed(2));
      $scope.payUseBalance = true;
      resume();
    });
    $scope.$root.$on('cancel-balance', function(event, data) {
      $scope.order.balance = 0;
      $scope.payUseBalance = false;
      resume();
    });
    $scope.$root.$on('pay-coupon', function(event, data) {
      $scope.order.coupon = parseFloat(parseFloat(data.amount).toFixed(2));
      $scope.order.coupon_code = data.coupon.code;
      $scope.payUseCoupon = true;
      resume();
    });
    $scope.$root.$on('cancel-coupon', function(event, data) {
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
  .controller('CouponPayCtrl', function($scope, $state, $window, $resource, $ionicScrollDelegate, $ionicHistory, User, Loading) {
    var total = parseFloat($state.params.total),
      query = function(type) {
        var resource = $resource(config.domain + '/mobile/coupons');
        Loading.show();
        resource.query({
          userid: User.current().id,
          type: type
        }, function(result) {
          $scope.coupons = [];

          _.each(result, function(coupon) {
            if (total >= coupon.minprice && total >= coupon.price) {
              $scope.coupons.push(coupon);
            }
          });
          $ionicScrollDelegate.resize();
          Loading.close();
        }, function(err) {
          console.log(err);
          Loading.tip('应用异常');
        });
      };

    $scope.total = total;
    $scope.pay = function(code) {
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
    $scope.cancel = function() {
      Loading.tip('已取消使用优惠券支付');
      $scope.$root.$broadcast('cancel-coupon');
      $ionicHistory.goBack();
    };

    query('unuse');
  })
  /*
   使用余额路由
   */
  .controller('BalanceCtrl', function($scope, $state, $filter, $window, $ionicHistory, $timeout, User, Loading) {
    var total = parseFloat(parseFloat($state.params.total).toFixed(2)),
      balance = parseFloat(parseFloat($state.params.balance).toFixed(2));

    $scope.total = total;
    $scope.balance = balance;
    $scope.use = balance > total ? total : balance;
    $scope.value = $scope.use;
    $scope.$watch('value', function(value, old) {
      var value = parseFloat(value.toFixed(2));

      if (value !== old && value <= $scope.balance) {
        $scope.use = value > total ? total : value;
      }
    });
    $scope.pay = function() {
      $scope.$root.$broadcast('pay-balance', {
        use: $scope.use,
        total: $scope.total
      });
      $ionicHistory.goBack();
    };
    $scope.cancel = function() {
      $scope.$root.$broadcast('cancel-balance');
      Loading.tip('已取消使用余额支付');
      $ionicHistory.goBack();
    };
  })
  /*
   我的优惠券路由
   */
  .controller('CouponsCtrl', function($scope, $state, $window, $ionicScrollDelegate, $resource, User, Loading) {
    var query = function(type) {
      var resource = $resource(config.domain + '/mobile/coupons');
      Loading.show();
      resource.query({
        userid: User.current().id,
        type: type
      }, function(result) {
        $scope.coupons = result;
        $ionicScrollDelegate.resize();
        Loading.close();
      }, function(err) {
        console.log(err);
        Loading.tip('应用异常');
      });
    };

    $scope.switch = function(type) {
      $ionicScrollDelegate.scrollTop();
      $scope.choose = type;
      query(type);
    };

    $scope.switch('unuse');
  })
  /*我的收藏Control*/
  .controller('FavoriteCtrl', function($scope, $state, $http, $ionicPopup, $ionicLoading, User, Favorite, Loading) {
    Loading.show()
    $http
      .get(config.domain + '/mobile/favorite', {
        params: {
          userid: User.current().id
        }
      })
      .success(function(result) {
        Loading.close();
        $scope.items = _.map(result.fav, function(item) {
          item.cover = config.domain + item.cover;
          return item;
        });
        $scope.stores = _.map(result.fav_store, function(item) {
          item.cover = config.domain + item.image;
          return item;
        });
        Favorite.mine = $scope.items;
        Favorite.scope = $scope;
      })
      .catch(function(data) {
        Loading.tip('应用异常');
      });
    $scope.switchStore = function() {
      $scope.switchItem = 'STORE';
    };
    $scope.switchProduct = function() {
      $scope.switchItem = 'PRODUCT';
    };
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };
    $scope.removeProduct = function(id) {
      var userId = null;
      var user = User.current();
      if (user) {
        userId = User.current().id;
      }

      Favorite.removeProduct(userId, id);
      $scope.items = _.reject($scope.items, function(item) {
        return item.id == id;
      });
    };
    $scope.removeStore = function(id) {
      var userId = null;
      var user = User.current();
      if (user) {
        userId = User.current().id;
      }

      Favorite.removeStore(userId, id);
      $scope.stores = _.reject($scope.stores, function(item) {
        return item.store_id === id;
      });
    };

    $scope.switchItem = 'STORE';
  })
  /*账户余额control*/
  .controller('CostCtrl', function($scope, $state, $timeout, $resource, $http, $ionicHistory, $ionicScrollDelegate, AliPay, User, Loading) {
    var costHelper = $resource(config.domain + '/mobile/balance'),
      alipayFinishCallback = function(args) {
        Loading.show(1);
        $http
          .get(config.domain + '/mobile/cost/status?userid=' + args.userID + '&price=' + args.price + '&maxid=' + args.maxID)
          .success(function(result) {
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
          .catch(function(error) {
            Loading.tip('网络或服务器出现错误');
            $ionicHistory.goBack();
          });
      };

    $scope.paying = false;
    $scope.$root.czprice = 0;
    $scope.minID = 9999999999;

    $scope.fetch = function() {
      costHelper.get({
          userid: User.current().id,
          minid: $scope.minID
        },
        function(data) {
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
        function(data) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          console.log(data);
          Loading.tip('网络异常');
        });
    };
    $scope.switch = function(type) {
      $scope.hasMore = true;
      $scope.choose = type;
      $ionicScrollDelegate.resize();

    };
    $scope.paying = false;
    $scope.chongzhi = function() {
      $scope.paying = false;

      Loading.show(1);
      var resource = $resource(config.domain + '/mobile/alipay_cz');
      resource.save({
          price: $scope.$root.czprice,
          userid: User.current().id
        },
        function(result) {
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
        function(result) {
          Loading.tip('提交订单失败');
          $scope.paying = false;
          console.log(result);
        }
      );
    };

    $scope.choose = 'ALL';
    $scope.balance = 0;
    $scope.$on('$ionicView.afterEnter', function() {
      $scope.$apply(function() {
        $scope.balances = [];
        $scope.minID = 9999999999;
        $scope.hasMore = true;
        $ionicScrollDelegate.scrollTop();
      })

    });
  })
  .controller('AddressEditCtrl', function($scope, $state, $resource, $rootScope, $ionicHistory, $http, MyAddress, $window, User, Loading) {
    $scope.saveNewAddress = function() {
      Loading.show();
      var address = $scope.addressModel;
      $http
        .post(config.domain + '/mobile/addaddress', address)
        .success(function(result) {
          Loading.close();
          if (result.flag == 1) {
            Loading.tip('保存成功');
            MyAddress.newAddress(result.msg, User.current().addresses);
            $ionicHistory.goBack();
            $scope.$emit('address:saveNewSuccess', {
              address: result.msg
            });
          } else {
            Loading.tip(data.msg);
          }
        })
        .catch(function() {
          Loading.close();
        })
    };

    $scope.addressSubmit = function() {
      var address = $scope.addressModel;
      if (address.region && address.address && address.name && address.mobile) {
        if ($scope.isCreate) {
          $scope.saveNewAddress();
        } else {
          $scope.saveModifyAddress();
        }
      } else {
        Loading.tip('地址信息输入不完整，请检查');
      }
    };

    $scope.saveModifyAddress = function() {
      Loading.show();
      var address = $scope.addressModel;
      $http
        .post(config.domain + '/mobile/updateaddress', address)
        .success(function(result) {
          Loading.close();
          if (result.flag == 1) {
            Loading.tip('保存成功');
            MyAddress.updateAddress(result.msg, User.current().addresses);
            $ionicHistory.goBack();
          } else {
            Loading.tip(result.msg);
          }
        })
        .catch(function() {
          Loading.close();
        })
    };

    $scope.changeProvince = function() {
      $scope.addressModel.street = "";
      $scope.addressModel.region = "";
      $scope.addressModel.city = "";
      $scope.cities = MyAddress.getCurrentCities($scope.addressModel);

    };

    $scope.changeCity = function() {
      $scope.addressModel.street = "";
      $scope.addressModel.region = "";
      $scope.regions = MyAddress.getCurrentRegions($scope.addressModel);

    };

    $scope.changeRegion = function() {
      $scope.addressModel.street = "";
      $scope.streets = MyAddress.getCurrentStreets($scope.addressModel);
    };

    if ($state.params.id) {
      var address = MyAddress.getAddressByID($state.params.id, User.current().addresses);
      $scope.provinces = MyAddress.getProvinces();
      $scope.cities = MyAddress.getCurrentCities(address);
      $scope.regions = MyAddress.getCurrentRegions(address);
      $scope.streets = MyAddress.getCurrentStreets(address);
      // $scope = _.extend($scope, _.pick(address, 'province','city','region','street'));
      $scope.addressModel = address;
      $scope.isCreate = false;
    } else {
      $scope.provinces = MyAddress.getProvinces();
      $scope.isCreate = true;
      $scope.addressModel = {
        province: '',
        city: '',
        userid: User.current().id,
        tel: '',
        mobile: '',
        name: ''
      };
    }
  })
  /*地址管理control*/
  .controller('AddressCtrl', function($scope, $state, $http, $resource, $rootScope, $ionicHistory, MyAddress, $window, User, Loading) {
    var user = User.current(),
      resource = $resource(config.domain + '/mobile/address'),
      fetch = function() {
        Loading.show();

        resource.query({
            userid: user.id
          },
          function(data) {
            Loading.close();
            user.addresses = data;
          },
          function(err) {
            console.log(err);
            Loading.tip('应用异常');
          });
      };

    $scope.modifyAddress = function(id) {
      $state.go('address-edit', {
        id: id
      });
    };

    $scope.newAddress = function() {
      $state.go('address-edit');
    };

    $scope.deleteAddress = function(id) {
      Loading.show();
      $http
        .post(config.domain + '/mobile/deladdress', {
          id: id
        })
        .success(function(data) {
          Loading.close();
          if (data.flag == 1) {
            MyAddress.delAddress(id, $scope);
            Loading.tip('删除成功');
          } else {
            Loading.tip(data.msg);
          }
        })
        .catch(function() {
          Loading.close();
        });
    };

    $scope.setAsDefault = function(id) {
      Loading.show();
      $http
        .post(config.domain + '/mobile/defaultaddress', {
          id: id
        })
        .success(function(data) {
          Loading.close();
          if (data.flag == 1) {
            Loading.tip('设置成功');
            MyAddress.setDefaultAddress(id, User.current().addresses);
            // $ionicHistory.goBack();
          } else {
            Loading.tip(data.msg);
          }
        })
        .catch(function() {
          Loading.close();
        })
    };

    $scope.user = user;
    fetch();
  })
  /*
   搜索路由
   */
  .controller('SearchResultCtrl', function($scope, $http, $state, $resource, Loading, SearchKeywords, User) {
    $scope.keyword = $state.params.keyword;
    $scope.hasMore = false;
    min = 999999999;
    $scope.searchProduct = function() {

      if ($scope.keyword.length > 0) {
        $scope.hasMore = false;
        SearchKeywords.add($scope.keyword);
        var params = {
          keywords: $scope.keyword,
          min: min
        };
        var location = User.getLocation();
        if (location) {
          params.x = location.x;
          params.y = location.y;
        }

        Loading.show();
        $http
          .get(config.domain + '/mobile/search', {
            params: params
          })
          .success(function(result) {
            Loading.close();
            if (result && result.items.length > 0) {
              var products = _.map(result.items, function(item) {
                item.img = config.domain + item.cover;
                return item;
              });

              min = result.items[result.items.length - 1];
              products = _.union($scope.products, products);
              $scope.hasMore = true;


            }

            $scope.$broadcast('scroll.infiniteScrollComplete');
          })
          .catch(function(error) {
            Loading.close();
              $scope.$broadcast('scroll.infiniteScrollComplete');
          });
      } else {
        Loading.tip('请输入要搜索的产品名称');
      }
    };
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };
    $scope.searchProduct();
  })

.controller('SectionsCtrl', function($scope, $http, User) {

    $scope.process = 'WORKING';
    Location
      .current()
      .then(function(result) {
        $scope.process = 'DONE';
        $scope.location = result;
      })
      .then(null, function(error) {
        Loading.tip(error);
        $scope.process = 'ERROR';
      });
  })
  .controller('StoresCtrl', function($q, $scope, $ionicBackdrop, $resource, $filter, $state, $ionicPopup, $http, $ionicModal, User, Loading, Favorite) {
    var location = User.getLocation();
    var query = {
      category: '',
      order: 'distance',
      area: ''
    };

    if (location) {
      query.x = location.x;
      query.y = location.y;
    }
    var orderBy = [];
    var fetchStores = function() {

      var deferred = $q.defer();
      $http
        .get(config.domain + '/mobile/stores', {
          params: query
        })
        .success(function(result) {
          $scope.stores = _.map(result.data, function(item) {
            item.image = config.domain + item.image;
            return item;
          });
          deferred.resolve();
        })
        .catch(function(error) {
          $scope.stores = [];
          deferred.resolve();
        });

      return deferred.promise;
    };

    var fetchAreas = function() {
      var deferred = $q.defer();
      var city = User.getCity();

      $http
        .get(config.domain + '/mobile/select_area', {
          params: {
            cid: city.id
          }
        })
        .success(function(result) {
          $scope.areas = result;
          deferred.resolve();
        })
        .catch(function(error) {
          deferred.resolve();
        });

      return deferred.promise;
    };

    var fetchServices = function() {
      var deferred = $q.defer();
      $http
        .get(config.domain + '/mobile/category_store')
        .success(function(result) {
          $scope.services = result;
          deferred.resolve(result);
        })
        .catch(function(error) {
          $scope.services = [];
          deferred.resolve([]);
        });
      return deferred.promise;
    };

    $scope.doFavorite = function(storeID) {
      var userID = null;
      var user = User.current();
      if (user) {
        userID = user.id;
      }

      if ($scope.favorite) {
        Favorite.removeStore(userID, storeID);
        Loading.tip('已取消收藏');
      } else {
        Favorite.favoriteStore(userID, storeID);
        Loading.tip('收藏成功');
      }

      $scope.favorite = !$scope.favorite;

    };

    $scope.showProduct = function(id) {
      $state.go('product', {
        id: id
      });
    };

    $scope.showOtherProduct = function(storeID) {
      $state.go('categories', {
        storeID: storeID
      });
    };

    $scope.navigate = function(storeID) {
      var exists = _.find($scope.stores, function(store) {
        return store.id === storeID;
      });

      if (exists) {
        $state.go('navigate', {
          x: exists.x,
          y: exists.y
        });
      }
    };

    $ionicModal
      .fromTemplateUrl('templates/area-modal.html', {
        scope: $scope
      })
      .then(function(modal) {
        $scope.areaModal = modal;
      });

    $ionicModal
      .fromTemplateUrl('templates/services-modal.html', {
        scope: $scope
      })
      .then(function(modal) {
        $scope.servicesModal = modal;
      });

    $scope.showStore = function(id) {
      $state.go('store', {
        id: id
      });
    };
    $scope.changeOrderBy = function() {
      // An elaborate, custom popup
      orderByModal = $ionicPopup.show({
        template: '<ion-list><ion-item ng-repeat="order in orders" ng-click="setOrderby(order.key);">{{order.value}}</ion-item></ion-list>',
        // title: 'Enter Wi-Fi Password',
        // subTitle: 'Please use normal things',
        scope: $scope,
        buttons: [{
          text: '取消',
          onTap: function(e) {
            orderByModal.close();
          }
        }]
      });
    };
    $scope.changeServices = function() {
      $scope.servicesModal.show();
    };
    $scope.closeServicesModal = function() {
      $scope.servicesModal.hide();
    };
    $scope.setService = function(serviceID) {
      $scope.service = _.find($scope.services, function(service) {
        return service.id === serviceID;
      });
      query.category = serviceID;
      if ($scope.servicesModal) {
        $scope.servicesModal.hide();
      }

      fetchStores();
    };
    $scope.changeArea = function() {
      $scope.areaModal.show();
    };
    $scope.setOrderby = function(key) {
      $scope.orderBy = _.find($scope.orders, function(order) {
        return order.key == key;
      });
      query.order = key;
      orderByModal.close();
      if(fetchStores){
        fetchStores();
      }
    };
    $scope.setArea = function(areaCode) {
      $scope.area = _.find($scope.areas, function(area) {
        return area.code == areaCode;
      });
      query.area = areaCode;
      $scope.areaModal.hide();
      fetchStores();
    };
    $scope.setAllService = function(fetch) {
      $scope.service = {
        name: '全部',
        code: ''
      };
      if ($scope.servicesModal) {
        $scope.servicesModal.hide();
      }
      query.category = '';

      if (fetchStores) {
        fetchStores();
      }
    };
    $scope.setAllArea = function(fetch) {
      $scope.area = {
        name: '区域',
        code: ''
      };
      if ($scope.areaModal) {
        $scope.areaModal.hide();
      }
      query.area = '';

      if (fetchStores) {
        fetchStores();
      }
    };
    $scope.closeAreaModal = function(areaCode) {
      $scope.areaModal.hide();
    };
    $scope.setAllArea();
    $scope.setAllService();

    Loading.show();
    $q.all([fetchAreas(), fetchServices()])
      .then(function() {
        return fetchStores();
      })
      .then(function() {
        Loading.close();
      })
      .then(null, function(error) {
        Loading.close();
        console.log(error);
      });

    $scope.orderBy = {
      key: 'distance',
      value: '离我最近'
    };
    $scope.category = '';
    $scope.setAllArea();
    $scope.orders = [{
      key: 'hot',
      value: '智能排序'
    }, {
      key: 'distance',
      value: '离我最近'
    }, {
      key: 'star',
      value: '评价最好'
    }];
    // $timeout(function() {
    //   $ionicBackdrop.release();
    // }, 1000);
  })

.controller('FeedbackCtrl', function($scope, $http, $ionicHistory, $state, User, Loading) {
  $scope.content = '';
  $scope.submit = function() {
    Loading.show();
    $http
      .post(config.domain + '/mobile/feedback', {
        content: $scope.content,
        userid: User.current().id
      })
      .success(function(result) {
        Loading.tip('已提交，感谢您的反馈');
        $ionicHistory.goBack();
      })
      .catch(function() {
        Loading.close();
      })
  }
})

.controller('ParkCarCtrl', function($scope, $ionicHistory, User, Loading) {
  var map = Map.instance('park');
  var location = User.getLocation();
  Loading.show();
  if (map) {
    Map.center(map, location);
    Map.setMainLocation(map, location);
    var local = new BMap.LocalSearch(map, {
      renderOptions: {
        map: map
      }
    });
    local.search("停车");
    Loading.close();
  } else {
    $ionicHistory.goBack();
  }
})

.controller('GasStationCtrl', function($scope, $ionicHistory, User, Loading) {
  var map = Map.instance('gasStation');
  var location = User.getLocation();
  Loading.show();

  if (map) {
    Map.center(map, location);
    Map.setMainLocation(map, location);
    var local = new BMap.LocalSearch(map, {
      renderOptions: {
        map: map
      }
    });
    local.search("加油");
    Loading.close();
  } else {
    $ionicHistory.goBack();
  }
})


.controller('OrderCoinCtrl', function($q, $scope, $ionicBackdrop, $resource, $filter, $state, $ionicPopup, $http, $ionicModal, User, Loading, Favorite) {
  var user = User.current();
  if (user) {
    Loading.show();

    $http
      .get(config.domain + '/mobile/get_item_service', {
        params: {
          uid: user.id
        }
      })
      .success(function(result) {
        Loading.close();
        $scope.items = result.msg;
      })
      .catch(function(error) {
        Loading.close();
      })
  }


})

.controller('LeaveReplyCtrl', function($q, $scope, $ionicHistory, $ionicPopup, $state, $http, User, Loading) {


  $scope.submit = function() {
    var user = User.current();
    if (user) {
      $http
        .post(config.domain + '/mobile/leave_topic_reply', {
          id: $state.params.id,
          replied_user_id: $state.params.repliedUserID,
          uid: user.id,
          content: $scope.content
        })
        .success(function(result) {
          if (result.flag === 1) {
            Loading.tip('已评论');
            $scope.$root.$broadcast('topic:leaveReplySuccess', {
              reply_id: result.id,
              content: $scope.content,
              replied_user_id: $state.params.repliedUserID,
              id: $state.params.id,
              replied_user_name: $state.params.repliedUserName,
              user_name: user.username,
              user_id: user.id
            });
          } else {
            Loading.tip('错误，请重试');
          }

          $ionicHistory.goBack();
        })
        .catch(function(error) {

        });
    }
  };

  $scope = _.extend($scope, $state.params);
  $scope.content = '';

})

.controller('OrderCoinDetailCtrl', function($q, $scope, $ionicBackdrop, $resource, $filter, $state, $window, $ionicPopup, $http, $ionicModal, User, Loading, Favorite) {
  var user = User.current();
  if (user) {
    Loading.show();

    $http
      .get(config.domain + '/mobile/get_item_service_detail', {
        params: {
          uid: user.id,
          id: $state.params.id
        }
      })
      .success(function(result) {
        Loading.close();
        $scope.item = result.msg;
      })
      .catch(function(error) {
        Loading.close();
      });
  }

  $scope.shareOrderCoin = function() {
    var title = '我在车装甲的订单卷是' + $scope.item.service_code + '，现在分享给你哦';
    $window.plugins.socialsharing.share(title, '车装甲', $scope.item.qrcode, null)
  };
})

.controller('MineCommentCtrl', function($q, $scope, $ionicBackdrop, $resource, $filter, $state, $window, $ionicPopup, $http, $ionicModal, User, Loading, Favorite) {
  var user = User.current();
  if (user) {
    Loading.show();

    $http
      .get(config.domain + '/mobile/mine_comment', {
        params: {
          uid: user.id
        }
      })
      .success(function(result) {
        Loading.close();
        $scope.comments = result.msg;
      })
      .catch(function(error) {
        Loading.close();
      });
  }
})

.controller('NavigateCtrl', function($scope, $state, $ionicHistory, User, Loading) {
    // 百度地图API功能
    // 百度地图API功能
    // var map = new BMap.Map("park");
    // map.centerAndZoom(new BMap.Point(116.404, 39.915), 11);
    // var local = new BMap.LocalSearch(map, {
    //  renderOptions:{map: map}
    // });
    // local.search("停车场");
    var map = Map.instance('navigate');
    var location = User.getLocation();
    Loading.show();

    if (map) {
      Map.center(map, location);
      var start = new BMap.Point(location.x, location.y);
      var end = new BMap.Point($state.params.x, $state.params.y);
      var driving = new BMap.DrivingRoute(map, {
        renderOptions: {
          map: map,
          autoViewport: true
        }
      });
      driving.search(start, end);
      Loading.close();
    } else {
      Loading.tip('没有获取到您的位置信息');
      $ionicHistory.goBack();
    }
  })
  .controller('ProfileCtrl', function($scope, $http, $state, $ionicPopup, $ionicHistory, User, Loading) {
    $scope.user = _.clone($scope.$root.user);
    $scope.fetch = function() {
      Loading.show();

      $http
        .get(config.domain + '/mobile/get_auto', {
          params: {
            uid: $scope.$root.user.id
          }
        })
        .success(function(result) {
          Loading.close();
          $scope.auto = result.msg || {
            'auto_id': null,
            'mileage': null,
            'buy_time': null,
            'chassis_num': null,
            'car_num': null,
            'brand_code': null,
            'brand_id': null,
            'created': null,
            'brand': []
          };
          $scope.brand = _.pluck(result.msg.brand, 'name').join(' ');
        })
        .catch(function(error) {})
    };

    $scope.modifyPhoto = function() {
      if (navigator.camera) {
        navigator.camera.getPicture(function(url) {
            $scope.$apply(function() {
              //$scope.imgs.push(url);
              //$scope.user.portraiturl = url;
              $scope.portrait = url;
            });
          },
          function(message) {
            Loading.tip('没有选择照片');
          }, {
            destinationType: Camera.DestinationType.DATA_URL,
            sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
            encodingType: Camera.EncodingType.JPEG,
            quantity: 50,
          });
      }
    };

    $scope.modifyNickName = function() {
      $scope.nickname = $scope.user.nickname;
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="text"  ng-model="$parent.nickname">',
        title: '修改昵称',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced',
          onTap: function(e) {
            //return $scope.user.nickname;
            //$scope.$root.user.nickname = $scope.nickname;
            $scope.user.nickname = $scope.nickname;
          }
        }, {
          text: '取消',
          onTap: function(e) {
            $scope.nickname = $scope.$root.user.nickname;
          }
        }]
      });
    };

    $scope.modifyBirthday = function() {
      $scope.birthday = $scope.user.birthday;
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="date" as-date  ng-model="$parent.birthday">',
        title: '修改出生日期',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced',
          onTap: function(e) {
            $scope.user.birthday = $scope.birthday;
          }
        }, {
          text: '取消'
        }]
      });
    };

    $scope.modifyBuyTime = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="date" as-date ng-model="auto.buy_time">',
        title: '修改购车日期',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced'
        }]
      });
    };

    $scope.modifyCreated = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="date" as-date ng-model="auto.created">',
        title: '修改上牌时间',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced'
        }]
      });
    };

    $scope.modifyCarNum = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="text" ng-model="auto.car_num">',
        title: '修改车牌号',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced',
          onTap: function(e) {
            if ($scope.user.nickname) {
              return $scope.user.birthday;
            } else {
              e.preventDefault();
            }
          }
        }, {
          text: '取消'
        }]
      });
    };

    $scope.modifyChassisNum = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="text" ng-model="auto.chassis_num">',
        title: '修改车架号',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced'
        }]
      });
    };

    $scope.modifyMileage = function() {
      $scope.removeModal = $ionicPopup.show({
        template: '<input type="number" ng-model="auto.mileage">',
        title: '修改里程',
        scope: $scope,
        buttons: [{
          text: '确定',
          type: 'button-balanced'
        }]
      });
    };

    $scope.$root.$on('brand:modifySuccess', function(event, args) {
      $scope.brand = _.pluck(args.brands, 'name').join(' ');
      $scope.auto.brand_id = args.brands[args.brands.length - 1].id;
    });
    $scope.modifyBrand = function() {
      $state.go('modify-brands');
    };

    $scope.save = function() {
      Loading.show();

      $http
        .post(config.domain + '/mobile/edit_profile', {
          auto_id: $scope.auto.auto_id,
          portrait: $scope.portrait,
          portraiturl: $scope.user.portraiturl,
          nickname: $scope.user.nickname,
          birthday: $scope.user.birthday || '',
          buy_time: $scope.auto.buy_time,
          car_num: $scope.auto.car_num,
          chassis_num: $scope.auto.chassis_num,
          brand_id: $scope.auto.brand_id,
          uid: $scope.user.id,
          mileage: $scope.auto.mileage,
          created: $scope.auto.created
        })
        .success(function(result) {
          Loading.tip('已保存');
          $scope.$root.user = $scope.user;
          $ionicHistory.goBack();
        })
        .catch(function(error) {})
    };

    $scope.portrait = null;
    $scope.fetch();
  })
  .controller('ModifyBrandsCtrl', function($scope, $http, $state, $ionicHistory, User, Loading) {
    $scope.modifyBrand = function() {
      Loading.show();

      $http
        .get(config.domain + '/mobile/get_brands')
        .success(function(result) {
          Loading.close();
          if (result.msg && result.msg.length > 0) {
            $scope.brands.push(result.msg);
          }
        })
        .catch(function(error) {})

    };

    $scope.changeBrand = function(index) {
      Loading.show();
      $http
        .get(config.domain + '/mobile/get_brands', {
          params: {
            id: $scope.idx[index].id
          }
        })
        .success(function(result) {
          Loading.close();
          if ($scope.brands.length >= index + 1) {
            $scope.brands.splice(index + 1, ($scope.brands.length - index));
          }

          if ($scope.idx.length >= index + 1) {
            $scope.idx.splice(index + 1, ($scope.idx.length - index));
          }

          if (result.msg && result.msg.length > 0) {
            $scope.brands.push(result.msg);
          }
        })
        .catch(function(error) {})
    };

    $scope.modifyBrand();
    $scope.brands = [];
    $scope.idx = [];
    $scope.save = function() {
      $ionicHistory.goBack();
      $scope.$root.$broadcast('brand:modifySuccess', {
        brands: _.clone($scope.idx)
      });
    }
  })
  .controller('ProfileEditCtrl', function($scope, $state, $ionicHistory, User, Loading) {
    $scope.user = _.clone($scope.$root.user);
    $scope.save = function() {

    };
  });
