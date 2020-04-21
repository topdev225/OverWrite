const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('Shopper\'s shop view', function () {
  /* auth */
  beforeEach(function () {
    cy.customLogin('shopper0', 'shopper0')
  })

  it('Is on / page without redirects', function () {
    cy.visit('/')
    cy.url().should('eq', `${HOST}/`)
  })

  it('Sees 8 products', function () {
    cy.get('[data-cy="ProductCard"]').should('have.length', 8)
  })
})
