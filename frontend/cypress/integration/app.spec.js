const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('Initial tests', function () {
  it('successfully loads', function () {
    cy.visit(`/`)
  })

  it('Is redirected to login page', function () {
    cy.url().should('eq', `${HOST}/login`)
  })

  it('Check login form', function () {
    const test = 'test'
    cy.get('[data-cy="login"]')
      .type(test)
      .should('have.value', test)
      .clear()

    cy.get('[data-cy="password"]')
      .type(test)
      .should('have.value', test)
      .clear()
  })
})
