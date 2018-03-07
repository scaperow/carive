angular.module('starter')
    .directive('compile', ['$compile', function ($compile) {
        return function (scope, element, attrs) {
            scope.$watch(
                function (scope) {
                    // watch the 'compile' expression for changes
                    return scope.$eval(attrs.compile);
                },
                function (value) {
                    // when the 'compile' expression changes
                    // assign it into the current DOM
                    element.html(value);

                    // compile the new DOM and link it to the current
                    // scope.
                    // NOTE: we only compile .childNodes so that
                    // we don't get into infinite loop compiling ourselves
                    $compile(element.contents())(scope);
                }
            );
        };
    }])

    .directive('scrollParent', function ($ionicScrollDelegate) {
        return {
            restrict: 'A',
            scope: {
                scrollParent: '@',
                direction: "@"
            },
            link: function (scope, element, attrs) {
                var geth = $ionicScrollDelegate.$getByHandle(scope.scrollParent),
                    sc;


                function applydrag(drag) {
                    console.log(drag);

                    if (sc) {
                        if (scope.direction == "y") {
                            geth.scrollTo(sc.left - drag.gesture.deltaX, 0, false);
                        }
                        else if (scope.direction == "x") {
                            geth.scrollTo(sc.top - drag.gesture.deltaY, 0, false);
                        }
                    }
                }

                element.on('drag', applydrag);
                element.on('dragstart', function (event) {
                    sc = geth.getScrollPosition();
                });

                element.on('dragend', function (event) {
                    sc = false;
                });
            }
        };
    })