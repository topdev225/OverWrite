const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('Superadmin login', function () {

  it('logins and redirected to /admin page', function () {
    cy.visit('/login')

    cy.get('[data-cy="login"]')
      .type('admin')
      .should('have.value', 'admin')

    cy.get('[data-cy="password"]')
      .type('12345678')
      .should('have.value', '12345678')

    cy.get('[data-cy="submit"]')
      .click()

    cy.url().should('eq', `${HOST}/admin`)
  })
})
