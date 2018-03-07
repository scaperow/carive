var Map = {
    scope: null,
    instance: function (id) {
        var map = new BMap.Map(id);
        var point = new BMap.Point(108.95344, 34.265657);
        map.centerAndZoom(point, 14);
        map.addControl(new BMap.ZoomControl());
        return map;
    },
    center: function (map, point) {
        var point = new BMap.Point(parseFloat(point.x), parseFloat(point.y));
        map.centerAndZoom(point, map.getZoom());
    },
    addStoreOverlay: function (map, store) {
        var point = new BMap.Point(store.x, store.y);
        var marker = new BMap.Marker(point);
        var icon = new BMap.Icon('http://www.eofan.com/style2/images/m/location3.png', new BMap.Size(30, 30));
        marker.setIcon(icon);
        marker.tag = 'STORE';
        map.addOverlay(marker);
        map.store = store;
        marker.addEventListener('click', function () {
            Map.scope.$broadcast('map:clickStoreOverlay', {store: this.store});
        });

        var rectangleOverlay = new RectangleOverlay(point, store.name, 'checkpoint-overlay');
        rectangleOverlay.map = map;
        rectangleOverlay.marker = marker;
        rectangleOverlay.store = store;
        rectangleOverlay.beforeInitialize(function (self) {
            Map.scope.$broadcast('map:clickStoreOverlay', {store: self.store});
        });
        map.addOverlay(rectangleOverlay);
    },
    setMainLocation: function (map, location) {
        var point = new BMap.Point(location.x, location.y);
        var marker = new BMap.Marker(point);

        var icon = new BMap.Icon('http://www.eofan.com/style2/images/m/location1.png', new BMap.Size(30, 30));
        marker.setIcon(icon);
        marker.tag = 'STORE';

        var rectangleOverlay = new RectangleOverlay(point, '我的位置', 'checkpoint-assertive-overlay');
        rectangleOverlay.map = map;
        rectangleOverlay.marker = marker;
        rectangleOverlay.beforeInitialize();
        map.addOverlay(rectangleOverlay);
        map.addOverlay(marker);
    },
    clearStoreOverlay: function (map) {
        var overlays = map.getOverlays();
        _.each(overlays, function (overlay) {
            map.removeOverlay(overlay);
        });
    }

};

var x_pi = parseFloat(3.14159265358979324 * 3000.0 / 180.0);
function convertLocation(ax, ay) {
    var x = parseFloat(ax), y = parseFloat(ay);
    var z = Math.sqrt(x * x + y * y) + 0.00002 * Math.sin(y * x_pi);
    var theta = Math.atan2(y, x) + 0.000003 * Math.cos(x * x_pi);
    var bd_lon = z * Math.cos(theta) + 0.0065;
    var bd_lat = z * Math.sin(theta) + 0.006;

    return new BMap.Point(bd_lon, bd_lat);
}

function RectangleOverlay(mapPoint, label, className) {
    this._mapPoint = mapPoint;
    this._label = label;
    this._className = className;
}
RectangleOverlay.prototype = new BMap.Overlay(); // 继承Overlay
RectangleOverlay.prototype.beforeInitialize = function (click) {
    this._overlayEl = document.createElement('div');
    this._overlayEl.className = this._className;
    this._overlayEl.style.zIndex = BMap.Overlay.getZIndex(this._mapPoint.lat);
    function attachClickEvent(self) {
        var self = self;
        if (click) {
            self._overlayEl.addEventListener('click', function(){
               click(self);
            });
        }
    };
    attachClickEvent(this);
};
RectangleOverlay.prototype.initialize = function (map) {
    this._map = map;

    this._labelEl = document.createElement('span');
    this._labelEl.className = this._className + '-label';
    this._labelEl.appendChild(document.createTextNode(this._label));
    this._overlayEl.appendChild(this._labelEl);

    this._map.getPanes().labelPane.appendChild(this._overlayEl);
    return this._overlayEl;
};


RectangleOverlay.prototype.draw = function () {
    // 按照正常位置来摆放自定义覆盖物会出现偏移现象
    // 因为覆盖物默认是以左上角为锚点"钉"在地图上的
    // |
    // | (覆盖物默认被定在这个点上,
    // |  造成视觉上的偏移)       -------
    // |  v                      |     |
    // |  o------                o------
    // |  |     |                ^
    // |  -------                (而我们需要达到的效果如上, 锚点还是原来的位置,
    // |                          只是需要将覆盖物偏移)
    // |
    // 因此我们必须对原有的位置做一些偏移来修正定点的位置
    var pixel = this._map.pointToOverlayPixel(this._mapPoint);
    // 计算矩形偏移
    var style = window.getComputedStyle(this._overlayEl);
    //var overlayWidthOffset = parseInt(pixel.x - (parseInt(style.width) / 2), 0);

    var overlayHeight = parseInt(style.height, 10);
    this._overlayEl.style.left = (pixel.x ) + 'px';
    this._overlayEl.style.top = (pixel.y - overlayHeight + 5) + 'px';
};
