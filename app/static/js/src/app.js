// // For some reason, importing jquery directly here is not working.
// // This hack is from here: https://github.com/excid3/esbuild-rails/issues/4
import "./jquery";

import 'bootstrap';
import 'bootstrap-table';
// // $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['cs-CZ'])

// // add service worker and other PWA things
// import "./pwa";

// // Start Sentry to log FE errors
// import "./sentry";


// Stimulus
import { Application } from "@hotwired/stimulus"

window.Stimulus = Application.start()
// window.Stimulus.debug = true

import BstableController from "../controllers/bstable_controller.js"
window.Stimulus.register('bstable', BstableController)

import ClickerController from "../controllers/clicker_controller.js"
window.Stimulus.register('clicker', ClickerController)

import EnableEditorController from "../controllers/enable_editor_controller.js"
window.Stimulus.register('enable-editor', EnableEditorController)

import EnableSelect2Controller from "../controllers/enable_select2_controller.js"
window.Stimulus.register('enable-select2', EnableSelect2Controller)

import RefreshController from "../controllers/refresh_controller.js"
window.Stimulus.register('refresh', RefreshController)

import SeePasswordController from "../controllers/see_password_controller.js"
window.Stimulus.register('see-password', SeePasswordController)

import RecipeReactionsController from "../controllers/recipe_reactions_controller.js"
window.Stimulus.register('recipe-reactions', RecipeReactionsController)

import SelectBadgesController from "../controllers/select_badges_controller.js"
window.Stimulus.register('select-badges', SelectBadgesController)

import SetDurationController from "../controllers/set_duration_controller.js"
window.Stimulus.register('set-duration', SetDurationController)

import ToggleDetailsController from "../controllers/toggle_details_controller.js"
window.Stimulus.register('toggle-details', ToggleDetailsController)

import VisibilityController from "../controllers/visibility_controller.js"
window.Stimulus.register('visibility', VisibilityController)

import Sortable from 'stimulus-sortable'
window.Stimulus.register('sortable', Sortable)

import Clipboard from 'stimulus-clipboard'
window.Stimulus.register('clipboard', Clipboard)

// Turbo
import * as Turbo from "@hotwired/turbo"
