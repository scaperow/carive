/**
 * Created by PAVEI on 30/09/2014.
 * Updated by Ross Martin on 12/05/2014
 */

angular.module('ionicLazyLoad', []);

angular.module('ionicLazyLoad')
    .directive('lazyScroll', ['$rootScope', '$timeout',
        function($rootScope, $timeout) {
            return {
                restrict: 'A',
                link: function ($scope, $element) {

                    var scrollTimeoutId = 0;

                    $scope.invoke = function () {
                        $rootScope.$broadcast('lazyScrollEvent');
                    };

                    $element.bind('scroll', function () {

                        $timeout.cancel(scrollTimeoutId);

                        // wait and then invoke listeners (simulates stop event)
                        scrollTimeoutId = $timeout($scope.invoke, 0);

                    });


                }
            };
        }])

    .directive('imageLazySrc', ['$document', '$timeout',
        function ($document, $timeout) {
            return {
                restrict: 'A',
                link: function ($scope, $element, $attributes) {

                    var deregistration = $scope.$on('lazyScrollEvent', function () {
                            //console.log('scroll');
                            if (isInView()) {
                                $element[0].src = $attributes.imageLazySrc; // set src attribute on element (it will load image)
                                deregistration();
                            }
                        }
                    );

                    function isInView() {
                        var clientHeight = $document[0].documentElement.clientHeight;
                        var clientWidth = $document[0].documentElement.clientWidth;
                        var imageRect = $element[0].getBoundingClientRect();
                        return  (imageRect.top >= 0 && imageRect.bottom <= clientHeight) && (imageRect.left >= 0 && imageRect.right <= clientWidth);
                    }

                    // bind listener
                    // listenerRemover = scrollAndResizeListener.bindListener(isInView);

                    // unbind event listeners if element was destroyed
                    // it happens when you change view, etc
                    $element.on('$destroy', function () {
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
            };
        }]);