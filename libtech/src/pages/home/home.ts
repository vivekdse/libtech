import { Component } from '@angular/core';

import { NavController } from 'ionic-angular';
import { PanchayatsPage } from '../panchayats/panchayats'

@Component({
    selector: 'page-home',
    templateUrl: 'home.html'
})
export class HomePage {
    panchayatsPage = PanchayatsPage;
    panchayats = []; // Placeholder for list of panchayats to fetch

    constructor(public navCtrl: NavController) {

    }
    gotoPanchayats() {
        this.navCtrl.push(PanchayatsPage)
    }
}
