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

      .state('index', {
      url: '/index',
      templateUrl: 'templates/index.html',
      controller: 'IndexCtrl'
    })

    .state('message', {
      url: '/message',
      validate: true,
      templateUrl: 'templates/message.html',
      controller: 'MessageCtrl'
    })

    .state('message-detail', {
      url: '/message-detail/:id',
      templateUrl: 'templates/message-detail.html',
      controller: 'MessageDetailCtrl'
    })

    .state('mine-comment', {
      url: '/mine-comment',
      templateUrl: 'templates/mine-comment.html',
      controller: 'MineCommentCtrl'
    })

    .state('sections', {
      url: '/sections',
      templateUrl: 'templates/sections-modal.html',
      controller: 'SectionsCtrl',
    })

    .state('search', {
      url: '/search',
      controller: 'SearchCtrl',
      templateUrl: 'templates/search.html'
    })

    .state('shopcar', {
     url: '/shopcar',
     controller: 'CarCtrl',
     templateUrl: 'templates/shopcar.html'
    })

    .state('categories', {
      url: '/categories/:storeID/:locateCategoryCode/:keyword/:type',
      templateUrl: 'templates/categories.html',
      controller: 'CategoriesCtrl'
    })

    .state('nearby', {
      url: '/nearby/:from',
      templateUrl: 'templates/nearby.html',
      controller: 'NearbyCtrl'
    })

    .state('car', {
      url: '/car',
      templateUrl: 'templates/cart.html',
      controller: 'CarCtrl'
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

    .state('gwzn', {
      url: '/gwzn',
      validate: true,
      templateUrl: 'templates/service-gwzn.html',
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
      templateUrl: 'templates/order-detail.html',
      controller: 'OrderDetailCtrl'
    })


    .state('order', {
      url: '/order',
      validate: true,
      templateUrl: 'templates/order.html',
      controller: 'OrderCtrl'
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

    .state('history', {
      url: '/history',
      validate: true,
      templateUrl: 'templates/history.html',
      controller: 'HistoryCtrl'
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

    .state('order-coin', {
      url: '/order-coin',
      validate: true,
      templateUrl: 'templates/order-coin.html',
      controller: 'OrderCoinCtrl'
    })

    .state('order-coin-detail', {
      url: '/order-coin-detail/:id',
      validate: true,
      templateUrl: 'templates/order-coin-detail.html',
      controller: 'OrderCoinDetailCtrl'
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
      templateUrl: 'templates/show-order.html',
      controller: 'ShowOrderCtrl'
    })

    .state('mine-show-order', {
      url: '/mine-show-order',
      validate: true,
      templateUrl: 'templates/mine-show-order.html',
      controller: 'MineShowOrderCtrl'
    })

    .state('question', {
      url: '/question',
      validate: true,
      templateUrl: 'templates/question.html',
      controller: 'QuestionCtrl'
    })

    .state('answer', {
      url: '/answer/:questionID',
      validate: true,
      templateUrl: 'templates/answer.html',
      controller: 'AnswerCtrl'
    })

    .state('modify-brands', {
      url: '/modify-brands',
      validate: true,
      templateUrl: 'templates/modify-brands.html',
      controller: 'ModifyBrandsCtrl'
    })

    .state('new-question', {
      url: '/new-question',
      validate: true,
      templateUrl: 'templates/new-question.html',
      controller: 'NewQuestionCtrl'
    })

    .state('gas-station', {
      url: '/gas-station',
      templateUrl: 'templates/gas-station.html',
      controller: 'GasStationCtrl'
    })

    .state('profile', {
      url: '/profile',
      templateUrl: 'templates/profile.html',
      controller: 'ProfileCtrl'
    })

    .state('profile-edit', {
      url: '/profile-edit',
      templateUrl: 'templates/profile-edit.html',
      controller: 'ProfileEditCtrl'
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
  .directive('asDate', function() {
    return {
      require: '^ngModel',
      restrict: 'A',
      link: function(scope, element, attrs, ctrl) {
        ctrl.$formatters.splice(0, ctrl.$formatters.length);
        ctrl.$parsers.splice(0, ctrl.$parsers.length);
        ctrl.$formatters.push(function(modelValue) {
          if (!modelValue) {
            return;
          }
          return new Date(modelValue);
        });
        ctrl.$parsers.push(function(modelValue) {
          return modelValue;
        });
      }
    }
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
