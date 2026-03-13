/******************************************************************************\
|                                                                              |
|                              mosquito-markers.js                             |
|                                                                              |
|******************************************************************************|
|                                                                              |
|        This defines a mixin for adding mosquito markers to a map.            |
|                                                                              |
|        Author(s): Abe Megahed                                                |
|                                                                              |
|        This file is subject to the terms and conditions defined in           |
|        'LICENSE.txt', which is part of this source code distribution.        |
|                                                                              |
|******************************************************************************|
|     Copyright (C) 2025, Data Science Institute, University of Wisconsin      |
\******************************************************************************/

import Browser from '../../utilities/web/browser.js';
import QueryString from '../../utilities/web/query-string.js';

export default {

	//
	// mapping functions
	//

	getClusterGroup: function(source) {
		return L.markerClusterGroup({
			options: Object.assign(L.MarkerClusterGroup.prototype.options, defaults.clustering),

			iconCreateFunction: function (cluster) {
				const markers = cluster.getAllChildMarkers();
				const numMarkers = markers.length;
				const iconSize = Math.trunc(15 + Math.log10(numMarkers) * 6);

				return new L.DivIcon({
					html: `<div>${numMarkers}</div>`,
					className: source.replace(/_/g, '-') + ' cluster',
					iconSize: new L.Point(iconSize, iconSize)
				});
			}
		});
	},

	getClusterGroups: function(sources) {
		let clusterGroups = {};
		for (let i = 0; i < sources.length; i++) {
			let source = sources[i];
			clusterGroups[source] = this.getClusterGroup(source);
		}
		return clusterGroups;
	},

	addMapMarker: function(map, source, observation, selected) {

		// get marker icon
		//
		if (!this.icons[source]) {
			this.icons[source] = new L.DivIcon({
				html: `<div></div>`,
				className: source.replace(/_/g, '-') + ' marker',
				iconSize: Browser.is_mobile? defaults.map.markerSize.mobile : defaults.map.markerSize.desktop
			});
		}
		let icon = this.icons[source];

		// create marker
		//
		let marker = L.marker([observation.y, observation.x], {
			icon: icon,
			source: source,
			id: observation.id
		});

		// save reference to marker
		//
		this.markers[observation.id] = marker;

		// add marker popup on click
		//
		marker.on('click', () => {
			this.addObservationPopup(marker);
		});

		// show selected marker
		//
		if (observation.id === selected) {
			this.addObservationPopup(marker);
		}

		// add marker to map
		//
		marker.addTo(map);
	},

	addMapMarkers: function(map, source, observations, selected) {
		for (let i = 0; i < observations.length; i++) {
			this.addMapMarker(map, source, observations[i], selected);
		}
	},

	addClusteredMarker: function(clusterGroup, source, observation, selected) {
		if (observation.x && observation.y) {
			let radius = Browser.is_mobile? defaults.map.markerSize.mobile / 2: defaults.map.markerSize.desktop / 2;

			// highlight single mosquito observation with additional data
			//
			if (observation.id == 'b9e9cbc7-2983-41d7-a041-59d42c50ee8e') {
				radius *= 2;
			}

			let marker = L.circleMarker([observation.y, observation.x], {
				source: source,
				id: observation.id,
				radius: radius,
				className: source.replace(/_/g, '-') + ' marker',
			});

			// save reference to marker
			//
			this.markers[observation.id] = marker;

			// add marker popup on click
			//
			marker.on('click', () => {
				this.addObservationPopup(marker);
			});

			// show selected marker
			//
			if (observation.id === selected) {
				this.addObservationPopup(marker);
			}

			// add marker to cluster
			//
			clusterGroup.addLayer(marker);
		}
	},

	locationInBounds(location, bounds) {
		if (bounds.lat) {
			if (location.y < bounds.lat.min || location.y > bounds.lat.max) {
				return false;
			}
		}
		if (bounds.lon) {
			if (location.x < bounds.lon.min || location.x > bounds.lon.max) {
				return false;
			}
		}
		return true;
	},

	addClusteredMarkers: function(map, source, observations, selected) {

		// create new cluster group, if necessary
		//
		if (!this.clusterGroups) {
			this.clusterGroups = this.getClusterGroups(this.sources);
		}
		let clusterGroup = this.clusterGroups[source];

		for (let i = 0; i < observations.length; i++) {
			let observation = observations[i];
			if (defaults.map.bounds) {
				if (this.locationInBounds(observation, defaults.map.bounds)) {
					this.addClusteredMarker(clusterGroup, source, observations[i], selected);
				}
			} else {
				this.addClusteredMarker(clusterGroup, source, observations[i], selected);
			}
		}

		// add cluster to map
		//
		map.addLayer(clusterGroup);

		return clusterGroup;
	},

	removeMarkers: function() {
		if (this.clusterGroups) {
			for (const source in this.clusterGroups) {
				let clusterGroup = this.clusterGroups[source];
				clusterGroup.clearLayers();
				this.map.removeLayer(clusterGroup);
			}
		}
	},

	showDataSource: function(dataSource) {
		this.$el.find('#map').removeClass('hide-' + dataSource);
	},

	hideDataSource: function(dataSource) {
		this.$el.find('#map').addClass('hide-' + dataSource);
	},

	//
	// rendering functions
	//

	addObservationMarkers: function(map, source) {
		let selected = QueryString.value('selected');

		this.fetchObservations(source, {

			// filter parameters
			//
			data: {
				countries: QueryString.value('countries'),
				before: QueryString.value('before'),
				after: QueryString.value('after'),
				genera: QueryString.value('genera'),
				species: QueryString.value('species')
			},

			// callbacks
			//
			success: (observations) => {
				// this.addMapMarkers(map, source, observations, selected);
				this.addClusteredMarkers(map, source, observations, selected);
			}
		});
	},

	addMarkers: function() {

		// store markers
		//
		this.markers = {};

		for (let i = 0; i < this.sources.length; i++) {
			let source = this.sources[i];
			this.addObservationMarkers(this.map, source);
		}
	},

	showMarkers: function() {
		this.removeMarkers();
		this.addMarkers();
	}
};
