const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('Shopper login', function () {

  it('logins and redirected to / page', function () {
    cy.visit('/login')

    cy.get('[data-cy="login"]')
      .type('shopper0')
      .should('have.value', 'shopper0')

    cy.get('[data-cy="password"]')
      .type('shopper0')
      .should('have.value', 'shopper0')

    cy.get('[data-cy="submit"]')
      .click()

    cy.url().should('eq', `${HOST}/`)
  })
})
