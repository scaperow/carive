angular
  .module('starter.controllers', ['ngResource', 'pasvaz.bindonce', 'base64'])
  /*
   程序入口
   */
  .run(function($rootScope, $state, $q, $ionicPopup, $ionicLoading, $resource, $http, $stateParams, $location, $ionicPlatform, $ionicHistory, $ionicModal, $window, $timeout, User, Loading, MyAddress) {
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
    $rootScope.xieyi = false;
    $rootScope.aggreeXieYi = function() {
      $rootScope.xieyi = true;
    };
    $ionicModal
      .fromTemplateUrl('templates/xieyi.html', {
        scope: $rootScope
      })
      .then(function(modal) {
        $rootScope.xieyiModal = modal;
      });
    $rootScope.closeXieYi = function() {
      $rootScope.xieyiModal.hide();
    };
    $rootScope.showXIEYI = function() {
      $rootScope.xieyiModal.show();
    };
    $rootScope.unaggreeXieYi = function() {
      $rootScope.xieyi = false;
    };
    $rootScope.closeLogin = function() {
      $rootScope.loginModal.hide();
    };
    $rootScope.call = function(tel) {
      window.location.href = 'tel://' + tel;
    };
    $rootScope.changeStatus = function(status) {
      $rootScope.registerModel = {};
      $rootScope.registerStoreModel = {};
      $rootScope.resetPasswordModel = {};
      $rootScope.loginModalStatus = status;
    };

    $rootScope.queryArea = function(pcode) {
      var deferred = $q.defer();
      Loading.show();
      $http
        .get(config.domain + '/mobile/getProvinces', {
          params: {
            pcode: pcode,
            site: 1
          }
        })
        .success(function(result) {
          deferred.resolve(result.msg);

          Loading.close();
        })
        .catch(function(error) {
          deferred.resolve([]);
        });

      return deferred.promise;
    };
    $rootScope.changeProvince = function() {
      $rootScope.registerStoreModel.city_code = "";
      $rootScope.registerStoreModel.area_code = "";

      var exists = _.find($rootScope.provinces, function(num) {
        return num.code === $rootScope.registerStoreModel.province_code
      });

      if (exists) {
        $rootScope.queryArea(exists.code)
          .then(function(result) {
            $rootScope.cities = result;
          });
      }

    };

    $rootScope.changeCity = function() {
      $rootScope.registerStoreModel.area_code = "";
      var exists = _.find($rootScope.cities, function(num) {
        return num.code === $rootScope.registerStoreModel.city_code
      });
      if (exists) {
        //$rootScope.registerStoreModel.area_code = exists.code;
        $rootScope.queryArea(exists.code)
          .then(function(result) {
            $rootScope.regions = result;
          });
      }
    };

    $rootScope.changeRegion = function() {
      //$rootScope.registerStoreModel.street = "";
      var exists = _.find($rootScope.regions, function(num) {
        return num.code === $rootScope.registerStoreModel.region
      });
      if (exists) {
        $rootScope.registerStoreModel.area_code = exists.code;
        //queryArea(exists.code)
        //  .then(function(result) {
        //    $scope.streets = result;
        //  });
      }
    };
    $rootScope.clickStoreImage = function(imgType) {
      $ionicPopup.confirm({
        title: '更换图片',
        cancelText: '取消',
        okText: '更换',
        okType: 'balanced'
      }).then(function(res) {
        if (res) {
          navigator.camera.getPicture(function(result) {
            if (imgType == 0) {
              $rootScope.image = result;
            } else if (imgType == 1) {
              $rootScope.image_license = result;
            } else if (imgType == 2) {
              $rootScope.image_legal = result;
            }
            //Loading.show();
            //$http
            //  .post(config.domain + '/store/change_cover', {
            //    source: result,
            //    sid: $scope.$root.user.store.id,
            //    uid: $scope.$root.user.id
            //  })
            //  .success(function(result) {
            //    Loading.close();
            //    $scope.cover = result;
            //  })
            //  .catch(function(error) {
            //
            //  });
          }, function(error) {

          }, {
            destinationType: Camera.DestinationType.DATA_URL,
            sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
            encodingType: Camera.EncodingType.JPEG,
            quantity: 70,
          });

        }
      });
    };

    $rootScope.registerStore = function() {
      if (!$rootScope.registerStoreModel.name) {
        return Loading.tip("请输入门店名称");
      }

      if ($rootScope.registerStoreModel.area_code == "") {
        Loading.tip("请选择门店所在省市区！");
      } else {
        Loading.show()

        if ($rootScope.registerStoreModel.image == "img/nopic.png") {
          $rootScope.registerStoreModel.image = ""
        }
        if ($rootScope.image) {
          $rootScope.registerStoreModel.image = $rootScope.image
        }

        if ($rootScope.registerStoreModel.image_license == "img/nopic.png") {
          $rootScope.registerStoreModel.image_license = ""
        }
        if ($rootScope.image_license) {
          $rootScope.registerStoreModel.image_license = $rootScope.image_license
        }

        if ($rootScope.registerStoreModel.image_legal == "img/nopic.png") {
          $rootScope.registerStoreModel.image_legal = ""
        }
        if ($rootScope.image_legal) {
          $rootScope.registerStoreModel.image_legal = $rootScope.image_legal
        }


        $http
          .post(config.domain + '/mobile/apply_store', $rootScope.registerStoreModel)
          .success(function(result) {
            if (result.flag === 1) {
              Loading.tip("申请成功，我们会在3个工作日内进行审核！");
            }
          })
          .catch(function(error) {

          });
      }
    };
    //$scope.changeStreet = function() {
    //  var exists = _.find($scope.streets, function(num) {
    //    return num.code === code
    //  });
    //  if (exists) {
    //    $scope.profile.area_code = exists.code;
    //  }
    //};

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
    // $rootScope.$on('loginFail', function(event, args) {
    //   $rootScope.changeStatus('LOGIN');
    //   $rootScope.show()
    // });
    $rootScope.$on('loginSuccess', function(event, args) {


      user = args.msg;
      $rootScope.user = user;
      if (!user.store) {
        $rootScope.loginModal.show();
        $rootScope.changeStatus('REGISTER_STORE');
        $rootScope.registerStoreModel.uid = user.id;
        $rootScope.registerStoreModel.image = "img/nopic.png";
        $rootScope.registerStoreModel.image_license = "img/nopic.png";
        $rootScope.registerStoreModel.image_legal = "img/nopic.png";
        $rootScope.image = ""
        $rootScope.image_license = ""
        $rootScope.image_legal = ""
        $rootScope.queryArea(0)
          .then(function(result) {
            $rootScope.provinces = result;
          });

      } else {
        if (user.store.check_state == 1) {
          $rootScope.loginModalStatus = 'LOGIN';
          $rootScope.resetPasswordModel = {};
          $rootScope.loginModel = {};
          $rootScope.registerModel = {};
          $rootScope.loginModal.hide();
        } else {
          $rootScope.changeStatus('REGISTER_STORE');
          $rootScope.registerStoreModel = user.store;
          $rootScope.registerStoreModel.uid = user.id

          $rootScope.image = ""
          $rootScope.image_license = ""
          $rootScope.image_legal = ""
          if (user.store.image == "")
            $rootScope.registerStoreModel.image = "img/nopic.png";
          if (user.store.image_license == "")
            $rootScope.registerStoreModel.image_license = "img/nopic.png";
          if (user.store.image_legal == "")
            $rootScope.registerStoreModel.image_legal = "img/nopic.png";

          $rootScope.queryArea(0)
            .then(function(result) {
              $rootScope.provinces = result;
            });
          if (user.store.province_code && user.store.province_code.length > 0) {
            $rootScope.queryArea(user.store.province_code)
              .then(function(result) {
                $rootScope.cities = result;
              });
          }
          if (args.msg.store.city_code && args.msg.store.city_code.length > 0) {
            $rootScope.queryArea(user.store.city_code)
              .then(function(result) {
                $rootScope.regions = result;
              });
          }

          $rootScope.loginModal.show();
        }
      }
    });
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

        if (localStorage.username && localStorage.password) {
          User.loginBackend();
        } else {
          $rootScope.changeStatus('LOGIN');
          $rootScope.loginModal.show();
        }
      });
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
            function(data) {
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


    $rootScope.login = function() {
      if ($rootScope.loginModel.userName && $rootScope.loginModel.password) {
        Loading.show();

        User
          .login($rootScope.loginModel.userName, hex_md5($rootScope.loginModel.password))
          .then(function(result) {
            var user = result.msg;

            Loading.close();
            User.syncProfile();

            if (!user.store) {
              $rootScope.changeStatus('REGISTER_STORE');
              $rootScope.registerStoreModel.uid = user.id;
              $rootScope.registerStoreModel.image = "img/nopic.png";
              $rootScope.registerStoreModel.image_license = "img/nopic.png";
              $rootScope.registerStoreModel.image_legal = "img/nopic.png";
              $rootScope.image = ""
              $rootScope.image_license = ""
              $rootScope.image_legal = ""
              $rootScope.queryArea(0)
                .then(function(result) {
                  $rootScope.provinces = result;
                });
            } else {
              if (user.store.check_state == 1) {
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
              } else {
                $rootScope.changeStatus('REGISTER_STORE');
                $rootScope.registerStoreModel = user.store;
                $rootScope.registerStoreModel.uid = user.id

                $rootScope.image = ""
                $rootScope.image_license = ""
                $rootScope.image_legal = ""
                if (user.store.image == "")
                  $rootScope.registerStoreModel.image = "img/nopic.png";
                if (user.store.image_license == "")
                  $rootScope.registerStoreModel.image_license = "img/nopic.png";
                if (user.store.image_legal == "")
                  $rootScope.registerStoreModel.image_legal = "img/nopic.png";

                $rootScope.queryArea(0)
                  .then(function(result) {
                    $rootScope.provinces = result;
                  });
                if (user.store.province_code && user.store.province_code.length > 0) {
                  $rootScope.queryArea(user.store.province_code)
                    .then(function(result) {
                      $rootScope.cities = result;
                    });
                }
                if (user.store.city_code && user.store.city_code.length > 0) {
                  $rootScope.queryArea(user.store.city_code)
                    .then(function(result) {
                      $rootScope.regions = result;
                    });
                }
              }
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
            if (!User.current() && $rootScope.loginModal) {
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

              //deferred.reject('账户不可用');
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
      if ($rootScope.loginModal) {
        $rootScope.loginModal.show();
        $rootScope.recoveryPasswordOnly = false;
      }
      // $rootScope.loginDeferred = args.deferred;
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
    $rootScope.recoverPassword = function() {
      $rootScope.loginModalStatus = 'RECOVERPASSWORD';
    };
    $ionicPlatform.ready(function() {

      var setTagsWithJPush = function(tags, alias) {
        if (window.plugins && window.plugins.jPushPlugin) {
          window.plugins.jPushPlugin.setTagsWithAlias(tags, alias);
        }
      };

    });


    $rootScope.$on('loginFail', function() {
      if ($rootScope.loginModal && $rootScope.loginModal.show) {
        $rootScope.loginModal.show();
      }
    });
    $rootScope.loginModalStatus = 'LOGIN';
    $rootScope.resetPasswordModel = {};
    $rootScope.loginModel = {};
    $rootScope.registerModel = {};
    $rootScope.tab = 0;
    //Map.scope = $rootScope;
  })
  .controller('IndexCtrl', function($scope, $ionicTabsDelegate, $ionicModal, $ionicSideMenuDelegate, $ionicScrollDelegate, $http, $state, ShopCar, Loading, User) {
    var resumeShopCarNumber = function() {
      $scope.$root.carNumber = ShopCar.all().length;
      // $scope.carNumber = new Date();
    };
    $scope.tab = 0;
    $scope.category = null;

    $scope.switch = function(tab) {
      // if (!User.current()) {
      //   $scope.$emit('user:requireLogin');
      // }
      $ionicTabsDelegate.select(tab);
      $scope.tab = tab;
      $ionicScrollDelegate.resize();
    };
    $scope.showProductSearch = function() {
      $state.go('search');
    };
    $scope.setLocation = function() {
      $state.go('regions');
    };
    $scope.$on('user:updateProfileSuccess', function() {
      resumeShopCarNumber();
    });
    $scope.$on('shopCar:addItemSuccess', function() {
      resumeShopCarNumber();
    });
    $scope.$on('shopCar:removeItemSuccess', function() {
      resumeShopCarNumber();
    });
    $scope.$on('tab:requestChange', function(event, args) {
      $ionicTabsDelegate.select(args.index);
      $scope.tab = args.index;
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
  .controller('HomeCtrl', function($scope, $resource, $state, $ionicPopup, $ionicListDelegate, $window, $filter, $timeout, $http, $location, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $ionicScrollDelegate, $q, Location, Ad, Products, Store, Loading, SearchKeywords, User, ShopCar) {
    $scope.goState = function(state) {
      $state.go(state);
    };
    $scope.$root.$on('loginSuccess', function() {
      var user = User.current();
      if (user) {
        $scope.score = user.score
        $scope.$root.user = user;
      } else {
        $scope.score = null;
      }

      $scope.refresh();
    });
    $scope.refresh = function() {
      if (!$scope.$root.user.store) {
        return;
      }

      var user = $scope.$root.user;
      if ($scope.$root.user) {
        $http
          .get(config.domain + '/mobile/store_summary', {
            params: {
              sid: user.store.id
            }
          })
          .success(function(result) {
            if (result.flag === 1) {
              $scope = _.extend($scope, result.msg);
            }

            $scope.$broadcast('scroll.refreshComplete');
          })
          .catch(function() {
            $scope.$broadcast('scroll.refreshComplete');
          });
      }
    }



    $scope.clickBlock = function(index) {
      $scope.$parent.switch(3);
      switch (index) {
        case 1:
          $scope.$parent.$broadcast('order:requireChangeTab', {
            name: 'all'
          });
          break;

        case 2:
          $scope.$parent.$broadcast('order:requireChangeTab', {
            name: 'unpay'
          });
          break;

        case 3:
          $scope.$parent.$broadcast('order:requireChangeTab', {
            name: 'undelivery'
          });
          break;

        case 4:
          $scope.$parent.$broadcast('order:requireChangeTab', {
            name: 'undelivery'
          });
          break;

        case 5:
          $scope.$parent.$broadcast('order:requireChangeTab', {
            name: 'success'
          });
          break;
      }
    }
  })
  .controller('CircleCtrl', function($scope, $state) {

  })
  .controller('CheckServiceCtrl', function($scope, $state) {
    $scope.$root.service_code = "";
    $scope.check_result = -1;
    $scope.check_result_msg = "";
    $scope.check_service_code = function() {
      console.log($scope.service_code);
      var user = User.current();
      if (true) {
        if (($scope.$root.service_code + '').length == 12) {
          $http
            .post(config.domain + '/mobile/check_service_code', {
              store_id: user.store.id,
              service_code: $scope.$root.service_code
            })
            .success(function(result) {
              if (result.flag == 1) {
                $scope.check_result = 1;
                $scope.check_result_msg = "";
              } else {
                $scope.check_result = 0;
                $scope.check_result_msg = result.msg;
              }
            })
            .catch(function(error) {
              if (error) {
                $scope.check_result = 0;
                $scope.check_result_msg = error.data.msg;
              } else {
                $scope.check_result = 0;
                $scope.check_result_msg = error;
              }
            });
        } else {
          $scope.check_result = 0;
          $scope.check_result_msg = "请输入12位的服务码！" + ($scope.$root.service_code + '').length;
        }
      } else {
        $scope.check_result = 0;
        $scope.check_result_msg = "请先登录！";
      }
    };
    $scope.scan = function() {
      cordova.plugins.barcodeScanner.scan(
        function(result) {
          $scope.$apply(function() {
            $scope.$root.service_code = result.text;
          });
        },
        function(error) {}
      );
    };
    $scope.history = function() {
      $state.go('service-history');
    };
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
          name: '撞到车映像'
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
      if (Location.available()) {
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
          })
      } else {
        $scope.progress = '不能打开您的定位';
        deferred.resolve();
      }

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
  .controller('ProductCtrl', function($scope, $http, $resource, $state, $window, $location, $ionicPopup, $ionicScrollDelegate, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {
    var refreshProduct = function() {
      Loading.show();
      $http
        .get(config.domain + '/mobile/product/' + $state.params.id)
        .success(function(product) {
          //var product = {"prompt": "", "storeName": "\u8f66\u88c5\u7532", "pid": 31, "standards": [{"psid": 37, "sku": "31", "name": "Mobil \u7f8e\u5b5a\u529b\u9738 \u8f66\u7528\u6da6\u6ed1\u6cb9 15W-50 4L API SJ\u7ea7 \u4f18\u8d28\u57fa\u7840\u6cb9 \u673a\u6cb9", "resume": "\u5feb\u901f\u542f\u52a8 \u9632\u6b62\u8150\u8680 \u51cf\u5c11\u673a\u6cb9\u635f\u8017 \u9ad8\u6e29\u4fdd\u62a4", "cover": "img/14527614811292.mobile.jpg", "price": 112.0, "standard": "", "pid": 31, "unit": "4L", "originalPrice": 139.0}], "sku": "31", "score": 0, "xgtotalnum": 0, "status": 1, "psid": 37, "resume": "\u5feb\u901f\u542f\u52a8 \u9632\u6b62\u8150\u8680 \u51cf\u5c11\u673a\u6cb9\u635f\u8017 \u9ad8\u6e29\u4fdd\u62a4", "price": 112.0, "standard": "4L", "flag": 1, "store_star_score": 4.0, "store_credit_score": 65.5, "name": "Mobil \u7f8e\u5b5a\u529b\u9738 \u8f66\u7528\u6da6\u6ed1\u6cb9 15W-50 4L API SJ\u7ea7 \u4f18\u8d28\u57fa\u7840\u6cb9 \u673a\u6cb9", "orginalprice": 139.0, "storeID": 1, "pics": [{"img": "img/14527614811292.mobile.jpg"}], "xgperusernum": 0, "time": 1452934937, "ourprice": 112.0, "quantity": 0}
          Loading.close();
          product.pics = _.map(product.pics, function(item) {
            //item.img = config.domain + item.img;
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
      ShopCar.put($scope.product);
      var user = User.current();

      if (user) {
        ShopCar.upload(user.id, ShopCar.all());
      }

      $state.go('cart');
      //$scope.$root.$broadcast('tab:changeToCart');
      //if (user) {
      //  ShopCar.upload(user.id, ShopCar.all());
      //}
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
      $state.go('products', {
        store: $scope.store.id,
        code: code
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
  .controller('StatisticsCtrl', function($scope, $resource, $state, $window, $location, $ionicPopup, $ionicScrollDelegate, $ionicSlideBoxDelegate, $ionicNavBarDelegate, $controller, $ionicHistory, $filter, User, Favorite, Products, ShopCar, Loading) {


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

      $scope.resumeForCopies = parseFloat($filter('number')(resume, 2));
      $scope.chooseCopies = checked.length;
    };
    $scope.showComments = function(psid) {
      $state.go($state.$current.name + '-comments', {
        psid: $scope.product.psid
      });
    };
    $scope.share = function(psid) {
      var title = '新鲜' + $scope.product.name + '只需' + $scope.product.price + ' 元,只在易凡网',
        url = 'http://www.eofan.com/product/' + psid;

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
  .controller('CategoriesCtrl', function($scope, $ionicModal, $http, $resource, $state, $q, $ionicScrollDelegate, $ionicSideMenuDelegate, $location, $timeout, Loading) {
    $scope.chooseCategory = null;
    $scope.owner = 1;
    $scope.salesOrderby = '';
    $scope.priceOrderby = '';
    $scope.storeID = $state.params.storeID;
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
    var fetchProducts = function() {
      var deferred = $q.defer();
      Loading.show();
      if ($scope.chooseCategory) {
        $http
          .get(config.domain + '/mobile/products', {
            params: {
              code: $scope.chooseCategory.id,
              sales: $scope.salesOrderby,
              price: $scope.priceOrderby,
              zy: $scope.owner,
              sid: $scope.storeID,
            }
          })
          .success(function(result) {
            $scope.products = _.map(result, function(item) {
              item.cover = config.domain + item.cover;
              return item;
            });
            deferred.resolve();
            Loading.close();
          })
          .catch(function() {
            Loading.close();
            deferred.resolve();
          });
      } else {
        Loading.close();
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
        $scope.fetchProducts();
      }
    });

    $scope.changeCategory = function() {
      $scope.categoryModal.show();
    };
    $scope.setCategory = function(name, code, id) {
      $scope.chooseCategory = {
        name: name,
        code: code,
        id: id
      };
      $scope.categoryModal.hide();
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
      Loading.show();
      fetchProducts();
    };


    fetchCategory()
      .then(fetchProducts);

  })
  /*
   * 查找control
   */
  .controller('SearchCtrl', function($scope, $state, $resource, Loading, SearchKeywords) {
    $scope.keyword = '';
    $scope.searchProduct = function() {
      if ($scope.keyword.length > 0) {
        SearchKeywords.add($scope.keyword);
        $state.go('search-result', {
          keyword: $scope.keyword
        });
      } else {
        Loading.tip('请输入搜索关键词', 1000);
      }
    };
    $scope.setKeyword = function(keyword) {
      $scope.keyword = keyword;
      $scope.searchProduct();
    };
    $scope.clearLocalKeyword = function() {
      SearchKeywords.clearLocalKeyword();
      $scope.keywords = SearchKeywords.local();
    };
    $scope.keywords = SearchKeywords.local();
    $scope.hots = SearchKeywords.hots();
  })
  .controller('ProductManagerCtrl', function($scope, $state, $resource, $http, $ionicPopup, $base64, Loading, User) {
    var m = null;
    $scope.hasMore = false;
    $scope.load = function() {
      $scope.hasMore = false;
      $http
        .get(config.domain + '/mobile/store/product/' + $scope.$root.user.id, {
          params: {
            min: m
          }
        })
        .success(function(result) {
          if (result && result.length > 0) {
            var products = _.map(result, function(item) {
              item.cover = config.domain + item.cover;
              return item;
            });

            $scope.products = _.union($scope.products, products);
            m = result[result.length - 1].psid;
            $scope.hasMore = true;
          }
        });
    };

    $scope.switchSHANGJIA = function() {
      $scope.status = 1;
      $scope.hasMore = true;
    };
    $scope.switchWEISHANGJIA = function() {
      $scope.status = 2;
      $scope.hasMore = true;
    };
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };
    $scope.updown = function(psid) {
      Loading.show();
      var status = 0;

      var product = _.find($scope.products, function(product) {
        return product.psid === psid;
      });


      if (product) {
        status = product.status;
        if (product.status === 1) {
          status = 2;
        } else {
          status = 1;
        }

        $http
          .post(config.domain + '/mobile/product_updown', {
            psid: psid,
            status: status
          })
          .success(function(result) {

            Loading.close();

            if (result.flag === 1) {
              Loading.tip('操作成功');
            }

            product.status = status;

          })
          .catch(function(error) {

          });
      }
    };

    $scope.status = 1;
    $scope.load();
  })
  /*用户中心control*/
  .controller('AccountCtrl', function($scope, $state, $resource, $http, $ionicPopup, $base64, Loading, User) {
    $scope.managerProduct = function() {
      $state.go('product-manager');
    };
    $scope.clickStoreCover = function() {
      $ionicPopup.confirm({
        title: '更换门店图片',
        cancelText: '取消',
        okText: '更换',
        okType: 'balanced'
      }).then(function(res) {
        if (res) {
          navigator.camera.getPicture(function(result) {
            Loading.show();
            $http
              .post(config.domain + '/store/change_cover', {
                source: result,
                sid: $scope.$root.user.store.id,
                uid: $scope.$root.user.id
              })
              .success(function(result) {
                Loading.close();
                $scope.cover = result;
              })
              .catch(function(error) {

              });
          }, function(error) {

          }, {
            destinationType: Camera.DestinationType.DATA_URL,
            sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
            encodingType: Camera.EncodingType.JPEG,
            quantity: 70,
          });

        }
      });
    };
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
          Loading.tip('网络或服务器异常');
        });
    };
    $scope.logout = function() {
      $scope.$root.user = null;
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
          $scope.$root.loginModal.show();
          //$state.go('index');
          // $scope.$emit('tab:requestChange',{
          //  index:0
          // });
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

              case 'unrecive':
              $scope.hasMore = _.where(result.items, {
                status: '待收货'
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
      query($scope.choose || 'unpay');
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
    $scope.$root.$on('dealOrder', function(event, args) {
        var exists = _.filter($scope.orders, function(order) {
            return order.id == args.id;
        });

        if (exists && exists.length > 0) {
            var exist = exists[0];
            exist.status = '正在处理';
        }
    });
        $scope.$root.$on('shouOrder', function(event, args) {
            var exists = _.filter($scope.orders, function(order) {
                return order.id == args.id;
            });

            if (exists && exists.length > 0) {
                var exist = exists[0];
                exist.status = '交易完成';
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
    $scope.choose = 'unpay';
    $scope.hasMore = true;
  })
  /*我的订单control*/
  .controller('StoreOrderCtrl', function($scope, $state, $resource, $ionicScrollDelegate, User, StoreOrders, Loading) {
    var query = function(type) {
      StoreOrders
        .query(User.current().store.id, $scope.index, $scope.size, type).$promise
        .then(function(result) {
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
        }, function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          Loading.tip('应用异常');
          console.log(error);
        });
    };
    //$scope.$parent.$broadcast('order:requireChangeTab',{name:'all'});
    $scope.$on('order:requireChangeTab', function(event, args) {
      $scope.choose = args.name;
    });
    $scope.load = function() {
      query($scope.choose || 'unpay');
    };
    $scope.switchOrderTab = function(choose) {
      $scope.hasMore = true;
      $scope.orders = [];
      $scope.choose = choose;
      $scope.index = 1;
      $scope.hasMore = true;
      $ionicScrollDelegate.scrollTop();
    };
    $scope.showDetail = function(oid, status) {
      $state.go('store-order-detail', {
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
    $scope.$root.$on('dealOrder', function(event, args) {
      var exists = _.filter($scope.orders, function(order) {
        return order.id == args.id;
      });

      if (exists && exists.length > 0) {
        var exist = exists[0];
        exist.status = '正在处理';
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
    $scope.choose = 'unpay';
    $scope.hasMore = true;
  })
  /*我的订单control*/
  .controller('StoreOrderYestodayCtrl', function($scope, $state, $resource, $ionicScrollDelegate, User, StoreOrders, Loading) {
    var query = function(type) {
      StoreOrders
        .query(User.current().store.id, $scope.index, $scope.size, type).$promise
        .then(function(result) {
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
        }, function(error) {
          $scope.$broadcast('scroll.infiniteScrollComplete');
          Loading.tip('应用异常');
          console.log(error);
        });
    };
    //$scope.$parent.$broadcast('order:requireChangeTab',{name:'all'});
    $scope.$on('order:requireChangeTab', function(event, args) {
      $scope.choose = args.name;
    });
    $scope.load = function() {
      query($scope.choose || 'unpay');
    };
    $scope.switchOrderTab = function(choose) {
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
    $scope.$root.$on('dealOrder', function(event, args) {
      var exists = _.filter($scope.orders, function(order) {
        return order.id == args.id;
      });

      if (exists && exists.length > 0) {
        var exist = exists[0];
        exist.status = '正在处理';
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
    $scope.choose = 'yestoday';
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
        deferred.resolve();
        return;

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
      $scope.balanceUsed = parseFloat($filter('number')(args.use, 2));
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
    $scope.wlgs = "";
    $scope.wldh = "";
    $scope.continuePay = function() {
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
      var resource = $resource(config.domain + '/mobile/cancelorder');
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

        resource = $resource(config.domain + '/mobile/cancelorder');
        resource.save({
          //status: 5,
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
    $scope.dealOrder = function() {
      var resource = $resource(config.domain + '/mobile/dealorder');
      if ($scope.order.statusValue == '1' || ($scope.order.paymentValue == '0' && $scope.order.statusValue == '0')) {

        $ionicPopup.show({
          title: '处理说明',
          template: '<p class="grey">处理后就可以进行发货处理了</p>',
          buttons: [{
            text: '处理订单',
            type: 'button-assertive',
            onTap: function() {
              Loading.show();
              resource = $resource(config.domain + '/mobile/dealorder');
              resource.save({
                id: $state.params.id,
              }, function(result) {
                if (result.err == 1) {
                  return Loading.tip(result.msg);
                }

                Loading.close();
                $scope.$root.$broadcast('dealOrder', {
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
      }
    };
    $scope.shouOrder = function() {
        var resource = $resource(config.domain + '/mobile/shouorder');
        if ($scope.order.statusValue == '3') {

            $ionicPopup.show({
                title: '收货说明',
                template: '<p class="grey">收货后就货款就直接付给商家了，您确定收到货物了吗？</p>',
                buttons: [{
                    text: '确定收货',
                    type: 'button-assertive',
                    onTap: function() {
                        Loading.show();
                        resource = $resource(config.domain + '/mobile/shouorder');
                        resource.save({
                            id: $state.params.id,
                        }, function(result) {
                            if (result.err == 1) {
                                return Loading.tip(result.msg);
                            }

                            Loading.close();
                            $scope.$root.$broadcast('shouOrder', {
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
        }
    };
    $scope.deliveryOrder = function() {
      var resource = $resource(config.domain + '/mobile/dealorder');
      if ($scope.order.statusValue == '2') {

        Loading.show();
        $http
          .get(config.domain + '/mobile/getDeliverys', {
            //params: {
            //  id: id
            //}
          })
          .success(function(result) {
            Loading.close();
            var template = '';
            template += '<select class="form-control gs" ng-model="$parent.wlgs" placeholder="物流公司" name="delivery" id="wlgs">';
            template += '    <option value="" selected="">物流公司</option>';
            _.each(result, function(item) {
              template += '    <option value="' + item.id + '" false="">' + item.name + '</option>';
            });
            template += '</select>';
            template += '<input type="text" ng-model="$parent.wldh" class=" dh" value="" id="wldh" style="margin-top:10px;" placeholder="物流单号">';
            $ionicPopup.show({
              title: '请填写物流信息，并确定',
              template: template,
              scope: $scope,
              buttons: [{
                text: '确定',
                type: 'button-assertive',
                onTap: function() {
                  Loading.show();
                  var did = $scope.wlgs;
                  var num = $scope.wldh;
                  if (did == "") {
                    Loading.tip("请选择物流公司");
                  } else if (num == "") {
                    Loading.tip("请填写物流单号");
                  } else {
                    resource = $resource(config.domain + '/mobile/deliveryOrder');
                    resource.save({
                      id: $state.params.id,
                      status: 3,
                      did: did,
                      num: num
                    }, function(result) {
                      if (result.flag == 1) {
                        return Loading.tip(result.msg);
                      }

                      Loading.close();
                      $scope.$root.$broadcast('deliveryOrder', {
                        id: $state.params.id
                      });
                      $ionicHistory.goBack();
                    }, function(error) {
                      Loading.tip('应用异常');
                      console.log(error);
                    });
                  }
                }
              }, {
                text: '取消'
              }]
            });
          })
          .catch(function(error) {
            console.log(error);
            Loading.tip("应用或服务器异常");
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

    /*店铺订单详情control*/
    .controller('StoreOrderDetailCtrl', function($scope, $state, $resource, $http, $ionicPopup, $ionicHistory, AliPay, MyOrders, Loading) {
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
        $scope.wlgs = "";
        $scope.wldh = "";
        $scope.continuePay = function() {
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
            var resource = $resource(config.domain + '/mobile/cancelorder');
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

                resource = $resource(config.domain + '/mobile/cancelorder');
                resource.save({
                    //status: 5,
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
        $scope.dealOrder = function() {
            var resource = $resource(config.domain + '/mobile/dealorder');
            if ($scope.order.statusValue == '1' || ($scope.order.paymentValue == '0' && $scope.order.statusValue == '0')) {

                $ionicPopup.show({
                    title: '处理说明',
                    template: '<p class="grey">处理后就可以进行发货处理了</p>',
                    buttons: [{
                        text: '处理订单',
                        type: 'button-assertive',
                        onTap: function() {
                            Loading.show();
                            resource = $resource(config.domain + '/mobile/dealorder');
                            resource.save({
                                id: $state.params.id,
                            }, function(result) {
                                if (result.err == 1) {
                                    return Loading.tip(result.msg);
                                }

                                Loading.close();
                                $scope.$root.$broadcast('dealOrder', {
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
            }
        };
        $scope.deliveryOrder = function() {
            var resource = $resource(config.domain + '/mobile/dealorder');
            if ($scope.order.statusValue == '2') {

                Loading.show();
                $http
                    .get(config.domain + '/mobile/getDeliverys', {
                        //params: {
                        //  id: id
                        //}
                    })
                    .success(function(result) {
                        Loading.close();
                        var template = '';
                        template += '<select class="form-control gs" ng-model="$parent.wlgs" placeholder="物流公司" name="delivery" id="wlgs">';
                        template += '    <option value="" selected="">物流公司</option>';
                        _.each(result, function(item) {
                            template += '    <option value="' + item.id + '" false="">' + item.name + '</option>';
                        });
                        template += '</select>';
                        template += '<input type="text" ng-model="$parent.wldh" class=" dh" value="" id="wldh" style="margin-top:10px;" placeholder="物流单号">';
                        $ionicPopup.show({
                            title: '请填写物流信息，并确定',
                            template: template,
                            scope: $scope,
                            buttons: [{
                                text: '确定',
                                type: 'button-assertive',
                                onTap: function() {
                                    Loading.show();
                                    var did = $scope.wlgs;
                                    var num = $scope.wldh;
                                    if (did == "") {
                                        Loading.tip("请选择物流公司");
                                    } else if (num == "") {
                                        Loading.tip("请填写物流单号");
                                    } else {
                                        resource = $resource(config.domain + '/mobile/deliveryOrder');
                                        resource.save({
                                            id: $state.params.id,
                                            status: 3,
                                            did: did,
                                            num: num
                                        }, function(result) {
                                            if (result.flag == 1) {
                                                return Loading.tip(result.msg);
                                            }

                                            Loading.close();
                                            $scope.$root.$broadcast('deliveryOrder', {
                                                id: $state.params.id
                                            });
                                            $ionicHistory.goBack();
                                        }, function(error) {
                                            Loading.tip('应用异常');
                                            console.log(error);
                                        });
                                    }
                                }
                            }, {
                                text: '取消'
                            }]
                        });
                    })
                    .catch(function(error) {
                        console.log(error);
                        Loading.tip("应用或服务器异常");
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
  .controller('CartCtrl', function($scope, $resource, $filter, $state, $ionicPopup, $http, User, ShopCar, Loading) {
    var resumeShopCarNumber = function() {
      $scope.$root.carNumber = ShopCar.all().length;
    };
    var fetchCarProduct = function() {
      ShopCar
        .fetchProduct()
        .then(function() {
          $scope.shopCarItems = ShopCar.all();
        });
    };

    $scope.$watch('shopCarItems', function() {
      $scope.hasCheckItems = _.where($scope.shopCarItems, {
        'checked': true
      }).length > 0;

      $scope.total = ShopCar.resumeTotalPrice($scope.shopCarItems);
    }, true);

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

    $scope.$on('tab:changeToCart', function() {
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
    //ShopCar.setOptionals([{
    //  "psid": 23,
    //  "type": 0,
    //  "pid": 14,
    //  "poid": 0,
    //  "quantity": 1
    //}, {
    //  "psid": 32,
    //  "type": 0,
    //  "pid": 23,
    //  "poid": 0,
    //  "quantity": 4
    //}])
    resumeShopCarNumber();
    fetchCarProduct();
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
            discountThreshold = parseFloat($filter('number')(result.discountthreshold, 2)) || 0;
            discount = parseFloat($filter('number')(result.discount, 2)) || 0;
            freeShippingFee = parseFloat($filter('number')(result.freeshippingfee, 2));
            shippingFee = parseFloat($filter('number')(result.shippingfee, 2));
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
          price =parseFloat(parseFloat((car.quantity * car.product.price), 2).toFixed(2)) ;
          $scope.order.price += price;
        });

        $scope.order.price = parseFloat($scope.order.price.toFixed(2));
        // $scope.renaminprice = $scope.order.currentprice = $scope.order.price + shippingFee;
        $scope.renaminprice = parseFloat(parseFloat($scope.order.price - $scope.order.balance - $scope.order.offPrice + $scope.order.shippingprice, 2).toFixed(2));
        $scope.order.currentprice = parseFloat(parseFloat($scope.order.price + $scope.order.shippingprice, 2).toFixed(2));
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

              }
            } else {
              Loading.tip('订单没有正确提交, 请到 我的订单 中确认');
            }
            ShopCar.clear();
            $ionicHistory.goBack();
          })
          .catch(function(error) {
            Loading.tip('订单已提交, 请及时支付');
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
      $scope.order.balance = parseFloat($filter('number')(data.use, 2));
      $scope.payUseBalance = true;
      resume();
    });
    $scope.$root.$on('cancel-balance', function(event, data) {
      $scope.order.balance = 0;
      $scope.payUseBalance = false;
      resume();
    });
    $scope.$root.$on('pay-coupon', function(event, data) {
      $scope.order.coupon = parseFloat($filter('number')(data.amount, 2));
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
    var total = parseFloat($filter('number')($state.params.total, 2)),
      balance = parseFloat($filter('number')($state.params.balance, 2));

    $scope.total = total;
    $scope.balance = balance;
    $scope.use = balance > total ? total : balance;
    $scope.value = $scope.use;
    $scope.$watch('value', function(value, old) {
      var value = $filter('number')(value, 2);

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
      $state.go($state.$current.name + '-product', {
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

    $scope.switchItem = 'PRODUCT';
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
            Loading.tip('充值没有成功');
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

    $scope.setAsDefault = function(id) {
      Loading.show();
      $http
        .post(config.domain + '/mobile/defaultaddress', {
          id: $state.param.id
        })
        .success(function(data) {
          Loading.close();
          if (data.flag == 1) {
            Loading.tip('设置成功');
            MyAddress.setDefaultAddress(id, User.current().addresses);
            $ionicHistory.goBack();
          } else {
            Loading.tip(data.msg);
          }
        })
        .catch(function() {
          Loading.close();
        })
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
            $ionicHistory.goBack();
          } else {
            Loading.tip(data.msg);
          }
        })
        .catch(function() {
          Loading.close();
        });
    };

    if ($state.params.id) {
      var address = MyAddress.getAddressByID($state.params.id, User.current().addresses);
      $scope.provinces = MyAddress.getProvinces();
      $scope.cities = MyAddress.getCurrentCities(address);
      $scope.regions = MyAddress.getCurrentRegions(address);
      $scope.streets = MyAddress.getCurrentStreets(address);
      // $scope = _.extend($scope, _.pick(address, 'province','city','region','street'));
      console.log($scope);
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
  .controller('AddressCtrl', function($scope, $state, $resource, $rootScope, $ionicHistory, MyAddress, $window, User, Loading) {
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

    $scope.user = user;
    fetch();
  })
  /*
   搜索路由
   */
  .controller('SearchResultCtrl', function($scope, $http, $state, $resource, Loading, SearchKeywords, User) {
    $scope.keyword = $state.params.keyword;
    $scope.hasMore = false;
    $scope.products = [];
    var min = 999999999;
    $scope.hasMoreDatas = function(){
      return $scope.hasMore;
    };
    $scope.searchProduct = function() {
         $scope.$broadcast('scroll.infiniteScrollComplete');

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

              min = result.items[result.items.length - 1].psid;
              $scope.products = _.union($scope.products, products);
              $scope.hasMore = true;
            }



          })
          .catch(function(error) {
            Loading.close();
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
    if (Location.available()) {
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
        })
    } else {
      $scope.process = 'DISABLE';
    }
  })
  .controller('StoresCtrl', function($q, $scope, $resource, $filter, $state, $ionicPopup, $http, $ionicModal, User, Store, Loading) {
    var query = {
      category: 0,
      order: 'distance',
      area: ''
    };
    var orderBy = [];

    var fetchStores = function() {
      var deferred = $q.defer();
      $http
        .get(config.domain + '/mobile/stores', {
          params: {

          }
        })
        .success(function(result) {
          $scope.stores = _.map(result.data, function(item) {
            item.image = config.domain + item.image;
            return item;
          });
          deferred.resolve();
        })
        .catch(function(error) {
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
    // Store
    //  .getStoresNearby()
    //  .then(function(result) {
    //   $scope.stores = result;
    //  });

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
        template: '<ion-list><ion-item ng-repeat="order in orders" ng-click="setOrderby(order.key)">{{order.value}}</ion-item></ion-list>',
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
    $scope.changeSections = function() {
      $scope.sectionsModal.show();
    };
    $scope.changeServices = function() {
      $scope.servicesModal.show();
    };
    $scope.closeSectionsModal = function() {
      $scope.sectionsModal.hide();
    };
    $scope.setSection = function(section) {
      $scope.sectionsModal.hide();
    };
    $scope.closeServicesModal = function() {
      $scope.servicesModal.hide();
    };
    $scope.setService = function(serviceCode) {
      $scope.service = _.find($scope.services, function(service) {
        return service.code === serviceCode;
      });
      $scope.servicesModal.hide();
    };
    $scope.changeArea = function() {
      $scope.areaModal.show();
    };
    $scope.setOrderby = function(key) {
      $scope.orderBy = _.find($scope.orders, function(order) {
        return order.key == key;
      });
      orderByModal.close();
    };
    $scope.setArea = function(areaCode) {
      $scope.area = _.find($scope.areas, function(area) {
        return area.code == areaCode;
      });
      $scope.areaModal.hide();
    };
    $scope.setAllService = function() {
      $scope.service = {
        name: '全部服务',
        code: ''
      };
      if ($scope.servicesModal) {
        $scope.servicesModal.hide();
      }
    };
    $scope.setAllArea = function() {
      $scope.area = {
        name: '全部区域',
        code: ''
      };
      if ($scope.areaModal) {
        $scope.areaModal.hide();
      }
    };
    $scope.closeAreaModal = function(areaCode) {
      $scope.areaModal.hide();
    };
    $scope.setAllArea();
    $scope.setAllService();

    $q.all([fetchAreas(), fetchServices()])
      .then(function() {
        return fetchStores();
      })
      .then(null, function(error) {
        console.log(error);
      });

    $scope.orderBy = {
      key: 'distance',
      value: '距离最近'
    };
    $scope.category = '';
    $scope.setAllArea();
    $scope.orders = [{
      key: 'distance',
      value: '距离最近'
    }, {
      key: 'star',
      value: '评价最高'
    }, {
      key: 'hot',
      value: '人气最旺'
    }];
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
  // 百度地图API功能
  // 百度地图API功能
  // var map = new BMap.Map("park");
  // map.centerAndZoom(new BMap.Point(116.404, 39.915), 11);
  // var local = new BMap.LocalSearch(map, {
  //  renderOptions:{map: map}
  // });
  // local.search("停车场");
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
    Loading.tip('没有获取到您的位置信息');
    $ionicHistory.goBack();
  }
})

/*
 * 校验服务码历史
 */
.controller('ServiceHistoryCtrl', function($scope, $state, $resource, $http, Loading, User) {
  $scope.historys = []
  $scope.searchHistory = function() {
    var user = User.current();
    if (user) {
      store_id = 1; //user.store.id
      Loading.show();
      $http
        .get(config.domain + '/mobile/service_code_history', {
          params: {
            store_id: 1
          }
        })
        .success(function(result) {
          //var result = {"msg": [{"items": [{"used_count": 1, "month": "12", "day": "22", "year": "2015"}], "month": "12", "year": "2015"}, {"items": [{"used_count": 1, "month": "11", "day": "21", "year": "2015"}], "month": "11", "year": "2015"}], "flag": 1}
          Loading.close();
          if (result.flag == 1) {
            $scope.historys = result.msg;
          } else {
            Loading.tip(result.msg);
          }
        })
        .catch(function(error) {
          Loading.close();
        });
    } else {
      Loading.tip("您还没登录，请先登录！");
    }
  };
  $scope.showHistoryDetail = function(id) {
    $state.go('service-history-detail', {
      id: id
    });
  };
  $scope.searchHistory();
})

.controller('QuestionCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $http, Loading, User) {
    var max_id = 99999999999999;
    $scope.hasMore = true;
    $scope.load = function() {
      $scope.hasMore = false;
      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .get(config.domain + '/mobile/question', {
            params: {
              userid: 0,
              max_id: max_id
            }
          })
          .success(function(result) {
            var questions = result.questions;
            if (questions.length > 0) {
              max_id = questions[questions.length - 1].id;
              $scope.hasMore = true;
              _.each(result.questions, function(question) {
                //var bests = _.where(result.bests, {
                //  question_id: question.id
                //});
                if (question.user_photo) {
                  question.user_photo = config.domain + question.user_photo;
                }
                //if (bests.length > 0) {
                //  question.best = bests[0];
                //
                //  if (question.best.user_photo) {
                //    question.best.user_photo = config.domain + question.best.user_photo;
                //  }
                //}
              });
            } else {
              $scope.hasMore = false;
            }
            $scope.questions = _.union($scope.questions, questions);
            Loading.close();
          })
          .catch(function() {

          })
      }
    };
    //$scope.load();
  })
  .controller('AnswerCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $http, Loading, User) {
    $scope.content = "";
    $scope.has_best = false;
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
            if (result.question.user_photo) {
              result.question.user_photo = config.domain + result.question.user_photo;
            }
            if (result.myanswer) {
              $scope.content = result.myanswer.content;
            }
            if (result.bests && result.bests.length > 0) {
              $scope.has_best = true;
            } else {
              $scope.has_best = false;
            }
            $scope.question = result.question;

            Loading.close();
          })
          .catch(function() {

          })
      } else {
        $scope.$emit('user:requireLogin');
      }
    };
    $scope.questionAnswer = function(questionID) {
      Loading.show();
      Loading.tip("回答成功！")
      var user = User.current();
      if (user) {
        Loading.show();
        $http
          .post(config.domain + '/mobile/question_answer', {
            uid: user.id,
            question_id: questionID,
            content: $scope.content
          })
          .success(function(result) {
            if (result.flag == 1) {
              //Loading.tip(result.msg);
              $state.go('answer-show', {
                questionID: questionID
              });
            }
          })
      }
    };

    fetch();
  })
  .controller('StoreBuyCtrl', function($scope, $ionicPopup, $state, $http, SearchKeywords, ShopCar) {
    $scope.keyword = '';
    $scope.$root.carNumber = ShopCar.all().length;
    if ($state.params.category) {
      $http
        .get(config.domain + '/mobile/ads_store_buy', {
          params: {

            cityID: '',
            category: $state.params.category
          }
        })
        .success(function(result) {
          var ads = _.map(result, function(item) {
            item.img = config.domain + '/upload/ad/' + item.img;
            //item.href = JSON.parse(item.href || null);
            return item;
          });;
          //推荐品牌
          $scope.brands = _.where(ads, {
            atype: 6
          });
          //特价区
          $scope.bargains = _.where(ads, {
            atype: 7
          });
          //推荐区
          $scope.recommands = _.where(ads, {
            atype: 8
          });
        })
        .catch(function() {

        });
    }

    $scope.searchProduct = function() {
      if ($scope.keyword.length > 0) {
        SearchKeywords.add($scope.keyword);
        $state.go('search-result', {
          keyword: $scope.keyword
        });
      } else {
        Loading.tip('请输入搜索关键词', 1000);
      }
    };
    $scope.showCategory = function(category) {
      $state.go('store_buy_category', {
        category: category
      });
    };
    $scope.search = function() {
      $state.go('search');
    };
    $scope.showSmallCategory = function(category) {
      $scope.keyword = category;
      $state.go('search-result', {
        keyword: $scope.keyword
      });
    };
    $scope.showCart = function() {
      $state.go('cart');
    };
    $scope.showDetail = function(id) {
      $state.go('product', {
        id: id
      });
    };

  })
  .controller('HelpCtrl', function($scope, $state) {
    $scope.htype = 0;
    $scope.showHelp = function(htype) {
      $scope.htype = htype;
    };
  })
  .controller('WithdrawCtrl', function($scope, $state, $http, Loading) {
    var max = 99999999999;
    $scope.load = function() {
      $scope.hasMore = false;
      $http
        .get(config.domain + '/mobile/withdraw_history', {
          params: {
            uid: $scope.$root.user.id,
            max: max,
            sid: $scope.$root.user.store.id
          }
        })
        .success(function(result) {
          if (result.flag === 1) {
            $scope.items = _.union(result.msg, $scope.items);

            if (result.msg.length > 0) {
              max = result.msg[result.msg.length - 1].id;
              $scope.hasMore = true;
            }
          }
        })
        .catch(function(error) {

        });
    };

    $scope.hasMore = true;
  })
  .controller('MineShowOrderCtrl', function($scope, $state, $ionicPopup, $ionicScrollDelegate, $http, Loading,User) {
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
                Loading.tip('操作失败');
          });
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
    $scope.leaveReply = function(id, repliedUserName, repliedUserID) {
      var user = User.current();

      if (user) {
        if (repliedUserID !== user.id) {
          $state.go('leave-reply', {
            id: id,
            repliedUserName: repliedUserName,
            repliedUserID: repliedUserID
          });
        }
      }
    };
    $scope.load = function() {
      $scope.hasMore = false;

      $http
        .get(config.domain + '/mobile/get_circle_topics', {
          params: {
            size: size,
            min: min,
            uid: User.current().id
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

          $scope.$broadcast('scroll.infiniteScrollComplete');
        })
        //.catch(function(error) {
        //  $scope.$broadcast('scroll.infiniteScrollComplete');
        //});
    };

    $scope.hasMore = false;
    $scope.circleTopics = [];
    $scope.load();
  })
  .controller('LeaveReplyCtrl', function($q, $scope, $ionicHistory, $state, $http, User, Loading) {
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
  .controller('BankCtrl', function($scope, $state, $ionicHistory, $http, $timeout, Loading, User) {
    $scope.load = function() {
      Loading.show();
      $http
        .get(config.domain + '/mobile/bank', {
          params: {
            uid: $scope.$root.user.id
          }
        })
        .success(function(result) {
          Loading.close();
          if (result.flag === 1) {
            $scope.bankModel = result.msg;
          }
        })
        .catch(function(error) {

        });

      // $scope.hasMore = false;
    };

    $scope.saveBank = function() {
      Loading.show();
      $http
        .post(config.domain + '/mobile/bind_bank', _.extend($scope.bankModel, {
          uid: $scope.$root.user.id
        }))
        .success(function(result) {
          //Loading.tip("绑定成功！");
          if (result && result.flag == 1) {
            Loading.tip("绑定成功！");
            $ionicHistory.goBack();
          } else {
            Loading.tip(result.msg);
          }
        })
        .catch(function(error) {

        });


    };
    $scope.showDetail = function() {
      $state.go('bank-detail');
    };
    $scope.$watch('bankModel.bank_account', function(oldValue, newValue) {
      if (oldValue !== newValue && newValue) {
        $http
          .get(config.domain + '/mobile/get_bank_name', {
            params: {
              no: $scope.bankModel.bank_account
            }
          })
          .success(function(result) {
            if (result.flag === 1 && result.msg) {
              $scope.bankModel.bank_name = result.msg.bank_name;
            } else {
              $scope.bankModel.bank_name = '';
            }
          })
      }
    });
    $scope.load();
    $scope.requestCode = function() {
      var user = User.current();
      var userName = user.username + '';
      if (userName.length != 11) {
        return Loading.tip('用户登录已过期');
      }

      User.requestValidationCodeRecovery(userName)
        .then(function(result) {
          $scope.counterWithRequestCode = 60;
          $scope.requestCodeProcessing = true;

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
          if (error.message) {
            Loading.tip(error.message);
          }
        });
    };
  })
  .controller('SettlementCtrl', function($scope, $state, $http, Loading) {
    var max = 999999999999;
    $scope.load = function() {
      $scope.hasMore = false;
      $http
        .get(config.domain + '/mobile/settlement_history', {
          params: {
            uid: $scope.$root.user.id,
            max: max,
            sid: $scope.$root.user.store.id
          }
        })
        .success(function(result) {
          if (result.flag === 1) {
            $scope.unsumeOrders = result.unsumeOrders;
            $scope.cashed_money = result.cashed_money;
            $scope.items = _.union(result.msg, $scope.items);

            if (result.msg.length > 0) {
              max = result.msg[result.msg.length - 1].id;
              $scope.hasMore = true;
            }
          }
        })
        .catch(function(error) {

        });
    };
    $scope.$on('$ionicView.afterEnter', function() {
      $scope.load();
    });
    $scope.showSettlementDetail = function() {
      $state.go('settlement-detail');
    };
    $scope.settlement = function() {
      $state.go('settlement-orders');
    };
    $scope.withdraw = function() {
      $state.go('withdraw-apply');
    };
    $scope.load();
  })
  .controller('WithdrawApplyCtrl', function($scope, $http, $state, $timeout, $q, Loading) {
    //$scope.load = function() {
    //    var result = {
    //      "data": {
    //        "alipay_truename": "谭利平",
    //        "alipay_account": "tanliping192@163.com",
    //        "bank_truename": "谭利平",
    //        "bank_name": "工商银行",
    //        "bank_branchname": "太白路支行",
    //        "bank_account": "6225 **** **** 7890"
    //      },
    //      "flag": 1,
    //      "msg": ""
    //    }
    Loading.show();
    $http
      .get(config.domain + '/mobile/store/get_bank', {
        params: {
          uid: $scope.$root.user.id
        }
      })
      .success(function(result) {
        $scope.item = result.data;
        $scope.hasMore = false;
        Loading.close();
      })
      .catch(function(error) {});
    //    $scope.item = result.data;
    //    $scope.hasMore = false;
    //};
    $scope.sendVCode = function() {
      $http
        .post(config.domain + '/mobile/store/cash', {
          uid: $scope.$root.user.id
        })
        .success(function(result) {
          if (result.flag === 1) {
            $scope.counterWithRequestCode = 60;
            $scope.requestCodeProcessing = true;

            var loop = function() {
              if (--$scope.counterWithRequestCode <= 0) {
                $scope.counterWithRequestCode = 60;
                $scope.requestCodeProcessing = false;
              } else {
                $timeout(loop, 1000);
              }
            };

            loop();
          }
        })
        .catch(function(error) {

        });
    };
    $scope.saveWithdraw = function() {
      if ($scope.money < 100) {
        return Loading.tip('抱歉，提现金额不能小于100元');
      }

      $http
        .post(config.domain + '/mobile/store/cash_sume', {
          uid: $scope.$root.user.id,
          money: $scope.money,
          code: $scope.code
        })
        .success(function(result) {
          if (result.flag === 1) {
            Loading.tip('申请成功，我们将在三个工作日内进行审核！');
          }
        })
        .catch(function(error) {

        });
    };
    $scope.code = '';
    $scope.money = 100;
  })
  .controller('ProfileStoreCtrl', function($scope, $state, $q, $http, MyAddress, Loading) {
    var queryArea = function(id) {
      var deferred = $q.defer();
      Loading.show();
      $http
        .get(config.domain + '/mobile/getProvinces', {
          params: {
            pcode: id,
            id: id,
            site: 1
          }
        })
        .success(function(result) {
          deferred.resolve(result.msg);

          Loading.close();
        })
        .catch(function(error) {
          deferred.resolve([]);
        });

      return deferred.promise;
    };

    var query = function() {
      if (!$scope.$root.user.store) {
        return;
      }

      Loading.show();

      $http
        .get(config.domain + '/mobile/store_profile', {
          params: {
            sid: $scope.$root.user.store.id
          }
        })
        .success(function(result) {
          Loading.close();
          if (result.flag === 1) {
            $scope.profile = result.msg;
            $scope.profile.province = $scope.profile.city = $scope.profile.region = $scope.profile.street = "";
            if ($scope.profile.area_code.length >= 4) {
              $scope.profile.province = $scope.profile.area_code.substring(0, 4);
            }
            if ($scope.profile.area_code.length >= 8) {
              $scope.profile.city = $scope.profile.area_code.substring(0, 8);
            }
            if ($scope.profile.area_code.length >= 12) {
              $scope.profile.region = $scope.profile.area_code.substring(0, 12);
            }
            if ($scope.profile.area_code.length >= 16) {
              $scope.profile.street = $scope.profile.area_code.substring(0, 16);
            }

            $scope.cities = _.filter($scope.profile.areas, function(area) {
              return area.code.length === 8;
            });
            $scope.regions = _.filter($scope.profile.areas, function(area) {
              return area.code.length === 12;
            });

            $scope.streets = _.filter($scope.profile.areas, function(area) {
              return area.code.length === 16;
            });

            $scope.provinces = [];
            queryArea(0)
              .then(function(result) {
                $scope.provinces = result;
              });
          }

        })
        .catch(function(error) {

        });
    };
    $scope.provinces = MyAddress.getProvinces();
    $scope.profileModel = {};

    $scope.saveProfileStore = function() {
      Loading.show()
      $http
        .post(config.domain + '/mobile/edit_store_profile', $scope.profile)
        .success(function(result) {
          if (result.flag === 1) {
            Loading.tip("保存成功！");
          }
        })
        .catch(function(error) {

        });

    };

    $scope.changeProvince = function() {
      $scope.profile.street = "";
      $scope.profile.region = "";
      $scope.profile.city = "";

      $scope.cities = [];
      $scope.regions = [];
      $scope.streets = [];

      var exists = _.find($scope.provinces, function(num) {
        return num.code === $scope.profile.province
      });

      if (exists) {
        $scope.profile.area_code = exists.code;
        queryArea(exists.code)
          .then(function(result) {
            $scope.cities = result;
          });
      }

    };

    $scope.changeCity = function() {
      $scope.profile.street = "";
      $scope.profile.region = "";
      $scope.regions = [];
      $scope.streets = [];

      var exists = _.find($scope.cities, function(num) {
        return num.code === $scope.profile.city
      });
      if (exists) {
        $scope.profile.area_code = exists.code;
        queryArea(exists.code)
          .then(function(result) {
            $scope.regions = result;
          });
      }
    };

    $scope.changeRegion = function() {
      $scope.profile.street = "";
      $scope.streets = [];
      var exists = _.find($scope.regions, function(num) {
        return num.code === $scope.profile.region
      });
      if (exists) {
        $scope.profile.area_code = exists.code;
        queryArea(exists.code)
          .then(function(result) {
            $scope.streets = result;
          });
      }
    };

    $scope.changeStreet = function() {
      var exists = _.find($scope.streets, function(num) {
        return num.code === code
      });
      if (exists) {
        $scope.profile.area_code = exists.code;
      }
    };

    query();
  })
  .controller('SettlementDetailCtrl', function($scope, $state, $http, $resource, $ionicScrollDelegate, Loading) {
    $scope.load = function() {
      $http
        .get(config.domain + '/mobile/settlement_detail', {
          params: {
            id: $state.params.id
          }
        })
        .success(function(result) {
          if (result.flag === 1) {
            $scope.deta = _.extend($scope, result.msg)
          }
        })
        .catch(function(error) {
          console.log(error);
        })
    };
    $scope.showDetail = function(oid) {
      $state.go('order-detail', {
        id: oid
      });
    };
    $scope.load();
  })
  .controller('SettlementOrdersCtrl', function($scope, $http, $state, $resource, $ionicHistory, $ionicScrollDelegate, Loading) {
    var max = 999999999999;
    $scope.load = function() {

      $scope.hasMore = false;
      $http
        .get(config.domain + '/mobile/settlement_order', {
          params: {
            uid: $scope.$root.user.id,
            max: max,
            sid: $scope.$root.user.store.id
          }
        })
        .success(function(result) {
          if (result.flag === 1) {
            $scope.orders = _.union(result.msg, $scope.orders);

            if (result.msg.length > 0) {
              max = result.msg[result.msg.length - 1].id;
              $scope.hasMore = true;
            }
          }
        })
        .catch(function(error) {

        });
    };
    $scope.showDetail = function(oid) {
      $state.go('order-detail', {
        id: oid
      });
    };
    $scope.checkAll = function(oid) {
      $scope.orders = _.map(function(order) {
        order.hasChecked = true;
        return order;
      })
    };
    $scope.settlement = function(oid) {
      var ids = JSON.stringify(_.pluck(_.where($scope.orders, {
        hasChecked: true
      }), 'id'));

      $http
        .post(config.domain + '/settlement/resume', {
          uid: $scope.$root.user.id,
          ids: ids
        })
        .success(function(result) {
          if (result.flag === 1) {
            Loading.tip('结算完成');
            $ionicHistory.goBack();

          } else {
            Loading.tip('结算失败');
          }
        });

    };
    $scope.hasMore = true;
  })
  .controller('ShowOrderCtrl', function($scope, $ionicPopup, $state, $ionicScrollDelegate, $timeout, $ionicHistory, $http, Loading, User) {
    $scope.imgs = [];
    $scope.content = '';

    var onSuccess = function(url) {
      $scope.$apply(function() {
        $scope.imgs.push(url);
      });
    };
    var onFail = function(message) {
      //Loading.tip(message);
      Loading.tip('用户取消或失败');
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
            $ionicHistory.goBack();
          })
          .catch(function(error) {

          })
      }
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
  });
