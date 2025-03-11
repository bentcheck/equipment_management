/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class StateIconField extends Component {
    static template = "it_equipment_management.StateIconField";

    get stateValue() {
        return this.props.record.data[this.props.name] || "";
    }

    getIconClass() {
        const value = this.stateValue.toString().toLowerCase();
        switch (value) {
            case "in_stock":
                return "fa fa-archive text-primary";
            case "assigned":
                return "fa fa-user text-primary";
            case "scrapped":
                return "fa fa-trash text-danger";
            default:
                return "";
        }
    }

    getTitle() {
        const value = this.stateValue.toString().toLowerCase();
        switch (value) {
            case "in_stock":
                return "In Stock";
            case "assigned":
                return "Assigned";
            case "scrapped":
                return "Scrapped";
            default:
                return "";
        }
    }
}

export const stateIconField = {
    component: StateIconField,
};

registry.category("fields").add("state_field", stateIconField);