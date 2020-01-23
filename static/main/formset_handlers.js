django.jQuery(document).on("google_point_map_widget:place_changed",
            function (e, place, lat, lng, locationInputElem, mapWrapID) {
                console.log(place); // Google geocoding response object
                console.log(locationInputElem); // django widget textarea widget (hidden)
                console.log(lat, lng);  // changed marker coordinates
                console.log(mapWrapID); // map widget wrapper element ID
        });

