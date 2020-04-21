const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('superadmin\'s product types list', function () {
  /* auth */
  beforeEach(function () {
    cy.customLogin()
  })

  it('Can access product types /add page', function () {
    cy.visit('/admin/product_types/add')
    cy.url().should('eq', `${HOST}/admin/product_types/add`)
  })

  it('There are buttons (close, create) and fields (name) on step 1', function () {
    cy.get('[data-cy="goToProductTypesWithoutSavingButton"]').should('exist').click()
    cy.url().should('eq', `${HOST}/admin/product_types`)
    cy.visit('/admin/product_types/add')

    cy.get('[data-cy="ProductTypeName"]')
      .should('exist')
      .type('pr-test-1')
      .should('have.value', 'pr-test-1')
      .clear()

    cy.get('[data-cy="createProductTypeButton"]')
      .should('exist')
      .click()
    cy.url().should('eq', `${HOST}/admin/product_types/add`)
    cy.get('[data-cy="ProductTypeName"]')
      .type('pr-test-1')
    cy.get('[data-cy="createProductTypeButton"]').click()
    cy.url().should('not.eq', `${HOST}/admin/product_types/add`)
  })

  it('There is "add new product type" button visible on the page', function () {
    cy.get('[data-cy="AddProductTypeItemButton"]').should('exist')
  })

  it('Click on "add new" leads to /add url', function () {
    cy.get('[data-cy="AddProductTypeItemButton"]').click()
    cy.url().should('eq', `${HOST}/admin/product_types/add`)
  })
})
