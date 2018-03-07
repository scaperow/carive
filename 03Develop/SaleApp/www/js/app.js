// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services'])
  .run(function($ionicPlatform) {
    $ionicPlatform.ready(function() {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      if (window.cordova && window.cordova.plugins.Keyboard) {
        cordoprova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      }

      if (window.StatusBar) {
        // org.apache.cordova.statusbar required
        StatusBar.styleDefault();
      }
    });
  })
  .config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider) {

    $stateProvider
    //.state('map', {
    //  url: '/map',
    //  templateUrl: 'templates/map.html',
    //  controller: 'HomeCtrl'
    //})
    //// setup an abstract state for the tabs directive
    //.state('room-summary', {
    //  url: "/room-summary/:lineID/:testRoomCode",
    //  controller: 'RoomSummaryCtrl',
    //  templateUrl: "templates/room-summary.html"
    //})

      .state('product-manager', {
      url: '/product-manager',
      templateUrl: 'templates/product-manager.html',
      controller: 'ProductManagerCtrl'
    })

    .state('statistics', {
      url: '/statistics',
      templateUrl: 'templates/statistics.html',
      controller: 'StatisticsCtrl'
    })

    .state('tongji', {
      url: '/tongji',
      templateUrl: 'templates/tongji.html',
      controller: 'StatisticsCtrl'
    })

    .state('index', {
      url: '/index',
      templateUrl: 'templates/index.html',
      controller: 'IndexCtrl'
    })

    .state('sections', {
      url: '/sections',
      templateUrl: 'templates/sections-modal.html',
      controller: 'SectionsCtrl'
    })

    .state('search', {
      url: '/search',
      templateUrl: 'templates/search.html',
      controller: 'SearchCtrl'
    })


    .state('categories', {
      url: '/categories/:storeID/:locateCategoryCode',
      templateUrl: 'templates/categories.html',
      controller: 'CategoriesCtrl'
    })

    .state('nearby', {
      url: '/nearby/:from',
      templateUrl: 'templates/nearby.html',
      controller: 'NearbyCtrl'
    })

    .state('cart', {
      url: '/cart',
      templateUrl: 'templates/order/cart.html',
      controller: 'CartCtrl'
    })

    .state('product-detail', {
      url: '/product/detail/:id',
      templateUrl: 'templates/pdetail.html',
      controller: 'PDetailCtrl'
    })

    .state('product-comments', {
      url: '/comments/:psid',
      validate: true,
      templateUrl: 'templates/comments.html',
      controller: 'CommentsCtrl'
    })

    .state('stores', {
      url: '/stores',
      templateUrl: 'templates/stores.html',
      controller: 'StoresCtrl'
    })


    .state('product', {
      url: '/product/:id',
      templateUrl: 'templates/product.html',
      controller: 'ProductCtrl'
    })

    .state('order-comment', {
      url: '/comment/:oiid/:psid',
      validate: true,
      templateUrl: 'templates/comment.html',
      controller: 'CommentCtrl'
    })

    .state('pay', {
      url: '/pay/:extra',
      validate: true,
      templateUrl: 'templates/payment.html',
      controller: 'PaymentCtrl'
    })

    .state('home-pay', {
      url: '/home-pay/:extra',
      validate: true,
      templateUrl: 'templates/payment.html',
      controller: 'PaymentCtrl'
    })

    .state('pay-address-edit', {
      url: '/pay-address-edit/:id',
      validate: true,
      templateUrl: 'templates/address-editor.html',
      controller: 'AddressEditCtrl'
    })

    .state('home-pay-address-edit', {
      url: '/home-pay-address-edit/:id',
      validate: true,
      templateUrl: 'templates/address-editor.html',
      controller: 'AddressCtrl'
    })

    .state('account', {
      url: '/account',
      validate: true,
      templateUrl: 'templates/account.html',
      controller: 'AccountCtrl'
    })

    .state('favorite', {
      url: '/favorite',
      validate: true,
      templateUrl: 'templates/favorite.html',
      controller: 'FavoriteCtrl'
    })

    .state('address', {
      url: '/address',
      validate: true,
      templateUrl: 'templates/address.html',
      controller: 'AddressCtrl'
    })

    .state('address-edit', {
      url: '/address-edit/:id',
      validate: true,
      templateUrl: 'templates/address-editor.html',
      controller: 'AddressEditCtrl'
    })

    .state('cost', {
      url: '/cost',
      validate: true,
      templateUrl: 'templates/cost.html',
      controller: 'CostCtrl'
    })

    .state('topup', {
      url: '/topup',
      templateUrl: 'templates/top-up.html',
      controller: 'CostCtrl'
    })

    .state('security', {
      url: '/security',
      validate: true,
      templateUrl: 'templates/security.html',
      controller: 'AccountCtrl'
    })

    .state('service', {
      url: '/service',
      validate: true,
      templateUrl: 'templates/service.html',
      controller: 'AccountCtrl'
    })

    .state('peisong', {
        url: '/peisong',
        validate: true,
        templateUrl: 'templates/service-psfw.html',
        controller: 'AccountCtrl'

      })
      .state('about', {
        url: '/about',
        validate: true,
        templateUrl: 'templates/about.html',
        controller: 'AccountCtrl'
      })

    .state('zffs', {
      url: '/zffs',
      validate: true,
      templateUrl: 'templates/service-zffs.html',
      controller: 'AccountCtrl'
    })

        .state('order-detail', {
            url: '/order-detail/:id',
            validate: true,
            templateUrl: 'templates/order/order-detail.html',
            controller: 'OrderDetailCtrl'
        })
        .state('store-order-detail', {
            url: '/store-order-detail/:id',
            validate: true,
            templateUrl: 'templates/order/store-order-detail.html',
            controller: 'StoreOrderDetailCtrl'
        })


    .state('order', {
      url: '/order',
      validate: true,
      templateUrl: 'templates/order/order.html',
      controller: 'OrderCtrl'
    })

      .state('store-order-yestoday', {
        url: '/store-order-yestoday',
        validate: true,
        templateUrl: 'templates/store_order/order-yestoday.html',
        controller: 'StoreOrderYestodayCtrl'
      })

      .state('pay-balance', {
        url: '/pay/balance/:balance/:total',
        hideTabs: true,
        templateUrl: 'templates/balance.html',
        controller: 'BalanceCtrl'
      })

    .state('pay-coupon', {
      url: '/pay/coupon/:total',
      hideTabs: true,
      templateUrl: 'templates/coupon-pay.html',
      controller: 'CouponPayCtrl'
    })

    .state('coupons', {
      validate: true,
      url: '/coupons',
      templateUrl: 'templates/coupons.html',
      controller: 'CouponsCtrl'
    })

    .state('search-result', {
      url: '/search-result/:keyword',
      templateUrl: 'templates/search-result.html',
      controller: 'SearchResultCtrl'
    })

    .state('reset-password', {
      url: '/reset-password',
      validate: true,
      templateUrl: 'templates/reset-password.html',
      controller: 'ResetPasswordCtrl'
    })

    .state('bind-mobile', {
      url: '/bind-mobile',
      templateUrl: 'templates/bind-mobile.html',
      controller: 'BindMobileCtrl'
    })

    .state('check-in', {
      url: '/check-in',
      validate: true,
      templateUrl: 'templates/check-in.html',
      controller: 'CheckInCtrl'
    })

    .state('trade', {
      url: '/trade',
      validate: true,
      templateUrl: 'templates/trade.html',
      controller: 'TradeCtrl'
    })

    .state('gifts', {
      url: '/gifts',
      validate: true,
      templateUrl: 'templates/gifts.html',
      controller: 'GiftsCtrl'
    })

    .state('continue-pay', {
      url: '/continue-pay/:id',
      validate: true,
      templateUrl: 'templates/continue-pay.html',
      controller: 'ContinuePayCtrl'
    })

    .state('pre-sale-detail', {
      url: '/pre-sale-detail',
      templateUrl: 'templates/pre-sale-detail.html',
      controller: 'PresaleCtrl'
    })


    .state('regions', {
      url: '/regions',
      templateUrl: 'templates/regions.html',
      controller: 'RegionsCtrl'
    })

    .state('store', {
      url: '/store/:id',
      templateUrl: 'templates/store.html',
      controller: 'StoreCtrl'
    })

    //违章查询
    .state('peccancy', {
        url: '/penccany',
        templateUrl: 'templates/peccancy.html',
        controller: 'IndexCtrl'
      })
      /*
       展示某一个门店下的商品
       */
      .state('products', {
        url: '/products/:store/:code',
        templateUrl: 'templates/products.html',
        controller: 'ProductsCtrl'
      })

    /*
     展示服务分类
     */
    .state('services-category', {
      url: '/services-category',
      templateUrl: 'templates/services-category.html',
      controller: 'ServicesCategoryCtrl'
    })

    /*
     展示服务列表
     */
    .state('services', {
      url: '/services',
      templateUrl: 'templates/services.html',
      controller: 'ServicesCtrl'
    })

    .state('feedback', {
      url: '/feedback',
      templateUrl: 'templates/feedback.html',
      controller: 'FeedbackCtrl'
    })

    .state('park', {
      url: '/park',
      templateUrl: 'templates/park.html',
      controller: 'ParkCarCtrl'
    })

    .state('navigate', {
      url: '/navigate/:x/:y',
      templateUrl: 'templates/navigate.html',
      controller: 'NavigateCtrl'
    })

    .state('service-history', {
        url: '/service-history',
        templateUrl: 'templates/order/service-history.html',
        controller: 'ServiceHistoryCtrl'
      })
      .state('service-history-detail', {
        url: '/service-history-detail',
        templateUrl: 'templates/order/service-history-detail.html',
        controller: 'ServiceHistoryDetailCtrl'
      })

    .state('question', {
      url: '/question',
      validate: true,
      templateUrl: 'templates/ask/question.html',
      controller: 'QuestionCtrl'
    })

    .state('answer', {
        url: '/answer/:questionID',
        validate: true,
        templateUrl: 'templates/ask/answer.html',
        controller: 'AnswerCtrl'
      })
      .state('answer-show', {
        url: '/answer-show/:questionID',
        validate: true,
        templateUrl: 'templates/ask/answer-show.html',
        controller: 'AnswerCtrl'
      })
      .state('store_buy_category', {
        url: '/store_buy_category/:category',
        validate: true,
        templateUrl: 'templates/store_buy/category.html',
        controller: 'StoreBuyCtrl'
      })
      .state('help', {
        url: '/help',
        validate: true,
        templateUrl: 'templates/other/help.html',
        controller: 'HelpCtrl'
      })
      .state('withdraw', {
        url: '/withdraw',
        validate: true,
        templateUrl: 'templates/store/withdraw.html',
        controller: 'WithdrawCtrl'
      })
      .state('withdraw-apply', {
        url: '/withdraw-apply',
        validate: true,
        templateUrl: 'templates/store/withdraw-apply.html',
        controller: 'WithdrawApplyCtrl'
      })
      .state('mine-show-order', {
        url: '/mine-show-order',
        validate: true,
        templateUrl: 'templates/store/mine-show-order.html',
        controller: 'MineShowOrderCtrl'
      })
      .state('leave-reply', {
        url: '/leave-reply/:id/:repliedUserName/:repliedUserID',
        validate: true,
        templateUrl: 'templates/leave-reply.html',
        controller: 'LeaveReplyCtrl'
      })
      .state('show-order', {
        url: '/show-order',
        validate: true,
        templateUrl: 'templates/store/show-order.html',
        controller: 'ShowOrderCtrl'
      })
      .state('bank', {
        url: '/bank',
        validate: true,
        templateUrl: 'templates/store/bank.html',
        controller: 'BankCtrl'
      })
      .state('bank-detail', {
        url: '/bank-detail',
        validate: true,
        templateUrl: 'templates/store/bank-detail.html',
        controller: 'BankCtrl'
      })
      .state('profile-store', {
        url: '/profile-store',
        validate: true,
        templateUrl: 'templates/store/profile-store.html',
        controller: 'ProfileStoreCtrl'
      })
      .state('settlement', {
        url: '/settlement',
        validate: true,
        templateUrl: 'templates/order/settlement.html',
        controller: 'SettlementCtrl'
      })
      .state('settlement-detail', {
        url: '/settlement-detail/:id',
        validate: true,
        templateUrl: 'templates/order/settlement-detail.html',
        controller: 'SettlementDetailCtrl'
      })
      .state('settlement-orders', {
        url: '/settlement-orders',
        validate: true,
        templateUrl: 'templates/order/settlement-orders.html',
        controller: 'SettlementOrdersCtrl'
      })
      .state('check-service', {
        url: '/check-service',
        validate: true,
        templateUrl: 'templates/order/check-service.html',
        controller: 'CheckServiceCtrl'
      })
      .state('invite', {
        url: '/invite',
        validate: true,
        templateUrl: 'templates/invite.html',
        controller: 'InviteCtrl'
      });


    // if none of the above states are matched, use this as the fallback
    $urlRouterProvider.otherwise('/index');

    //$ionicConfigProvider.views.transition('android');
    //Always use iOS style for all platform
    $ionicConfigProvider.tabs.style('standard');
    $ionicConfigProvider.tabs.position('bottom');
    $ionicConfigProvider.backButton.text('');
    $ionicConfigProvider.backButton.previousTitleText(false);

  })
  .directive('ngStars', function() {
    return {
      restrict: 'E',
      scope: {
        counter: '='
      },
      template: '<span>' + '<i class="icon ion-ios7-star" ng-class="counter >= 1 ? \'energized\': \'stable\'"></i>' + '<i class="icon ion-ios7-star" ng-class="counter >= 2 ? \'energized\': \'stable\'"></i>' + '<i class="icon ion-ios7-star" ng-class="counter >= 3 ? \'energized\': \'stable\'"></i>' + '<i class="icon ion-ios7-star" ng-class="counter >= 4 ? \'energized\': \'stable\'"></i>' + '<i class="icon ion-ios7-star" ng-class="counter >= 5 ? \'energized\': \'stable\'"></i>' + '</span>',
      replace: true
    };
  })
  .directive('lazyScroll', function($rootScope, $timeout) {
    return {
      restrict: 'A',
      link: function($scope, $element) {

        var scrollTimeoutId = 0;

        $scope.invoke = function() {
          $rootScope.$broadcast('lazyScrollEvent');
        };

        $element.bind('scroll', function() {
          console.log('aa');
          $timeout.cancel(scrollTimeoutId);

          // wait and then invoke listeners (simulates stop event)
          scrollTimeoutId = $timeout($scope.invoke, 0);

        });


      }
    }
  })
  .directive('imageLazySrc',
    function($document, $timeout) {
      return {
        restrict: 'A',
        link: function($scope, $element, $attributes) {

          var deregistration = $scope.$on('lazyScrollEvent', function() {
            //console.log('scroll');
            if (isInView()) {
              $element[0].src = $attributes.imageLazySrc; // set src attribute on element (it will load image)
              deregistration();
            }
          });

          function isInView() {
            var clientHeight = $document[0].documentElement.clientHeight;
            var clientWidth = $document[0].documentElement.clientWidth;
            var imageRect = $element[0].getBoundingClientRect();
            return (imageRect.top >= 0 && imageRect.bottom <= clientHeight) && (imageRect.left >= 0 && imageRect.right <= clientWidth);
          }

          // bind listener
          // listenerRemover = scrollAndResizeListener.bindListener(isInView);

          // unbind event listeners if element was destroyed
          // it happens when you change view, etc
          $element.on('$destroy', function() {
            deregistration();
          });

          // explicitly call scroll listener (because, some images are in viewport already and we haven't scrolled yet)
          $timeout(function() {
            if (isInView()) {
              $element[0].src = $attributes.imageLazySrc; // set src attribute on element (it will load image)
              deregistration();
            }
          }, 500);
        }
      }
    });
