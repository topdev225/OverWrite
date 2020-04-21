// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

import 'cypress-localstorage-commands'

const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

Cypress.Commands.add('customLogin', (username = 'admin', password = '12345678') => {
  // seed a post in the DB that we control from our tests
  return cy.request('POST', `${API_URL}/login`, {
    username,
    password
  }).its('body').as('user').then(function () {
    cy.setLocalStorage('user', this.user.token)
    cy.setLocalStorage('user_id', String(this.user.account_id))
    return cy.request({
      method: 'GET',
      url: `${API_URL}/accounts/${this.user.account_id}`,
      headers: {
        Authorization: `Bearer ${this.user.token}`,
        'X-Fields': '*'
      }
    })
  })
})
