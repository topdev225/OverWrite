import Vue from 'vue'
import Router from 'vue-router'

import AccountAddEdit from '@/components/Account/AccountAddEdit'
import AccountList from '@/components/Account/AccountList'
import CampaignAddEdit from '@/components/Campaign/CampaignAddEdit'
import CampaignList from '@/components/Campaign/CampaignList'
import ProductAttributeAddEdit from '@/components/ProductAttribute/ProductAttributeAddEdit'
import ProductAttributeList from '@/components/ProductAttribute/ProductAttributeList'
import DistributorAddEdit from '@/components/Distributor/DistributorAddEdit'
import DistributorList from '@/components/Distributor/DistributorList'
import OrderList from '@/components/Order/OrderList'
import OrderView from '@/components/Order/OrderView'
import ProductAddEdit from '@/components/Product/ProductAddEdit'
import ProductList from '@/components/Product/ProductList'
import ProductView from '@/components/Product/ProductView'
import ProductTypeAddEdit from '@/components/ProductType/ProductTypeAddEdit'
import ProductTypeList from '@/components/ProductType/ProductTypeList'
import TheHomePage from '@/components/TheHomePage'
import TheLoginPage from '@/components/TheLoginPage'
import TheNotFoundPage from "../components/TheNotFoundPage";
import VendorAddEdit from '@/components/Vendor/VendorAddEdit'
import VendorList from '@/components/Vendor/VendorList'

import axios from '@/axios'
import store from '@/store'
import {SUPERADMIN_ROLE_ID} from "@/config";


// import Cart from '@/components/Orders/Cart'
// import EditImages from '@/components/Catalog/EditImages'
// import EditImagesVariant from '@/components/Catalog/EditImagesVariant'
// import OrderConfirmation from '@/components/Orders/OrderConfirmation'
// import Report from '@/components/Reports/Report'
// import Storefront from '@/components/Orders/Storefront'
// import StorefrontPreview from '@/components/Catalog/StorefrontPreview'
// import VariantAdd from '@/components/Catalog/VariantAdd'
// import VariantEdit from '@/components/Catalog/VariantEdit'

Vue.use(Router);

// helpers
function withPrefix(prefix, routes) {
  return routes.map(route => {
    route.path = prefix + route.path;
    return route;
  })
}

// middleware
function requireToken(to, from, next) {
  // allow access to only certain paths without authentication
  const PATHS_WITHOUT_AUTHENTICATION = ['/login', '/order_confirmation'];

  if (PATHS_WITHOUT_AUTHENTICATION.indexOf(to.fullPath) > -1) {
    return next();
  }

  if (!localStorage.getItem('token') || !localStorage.getItem('userId')) {
    return next('/login');
  } else if (!store.state.account) {
    // login information was in localStorage, but state is empty. this can happen if the user hard-
    // reloads the page with Ctrl+R, for example. in this case, we want to fetch the account from
    // the API and proceed as if we just came from the login page.
    store.dispatch(
      'jv/get',
      [`accounts/${localStorage.getItem('userId')}`, {params: {include: 'role'}}],
    ).then(account => {
      // save the new account information in localStorage
      store.dispatch('login', account);
    });
  }

  return next();
}

function requireRole(allowedRoleNames, redirectTo) {
  // allow access to certain components only if the user has a particular role
  return (to, from, next) => {
    let roleName = localStorage.getItem('roleName');

    if (roleName && allowedRoleNames.indexOf(roleName) > -1) {
      return next();
    } else {
      store.dispatch('raiseError', 'Access denied');
      return next(redirectTo);
    }
  };
}

// routes
let accountRoutes = [
  {
    path: '/accounts',
    name: 'account_list',
    component: AccountList,
  },
  {
    path: '/accounts/add',
    name: 'account_add',
    component: AccountAddEdit,
  },
  {
    path: '/accounts/:id',
    name: 'account_edit',
    component: AccountAddEdit,
  },
];

let distributorRoutes = [
  {
    path: '/distributors',
    name: 'distributor_list',
    component: DistributorList,
  },
  {
    path: '/distributors/add',
    name: 'distributor_add',
    component: DistributorAddEdit,
    beforeEnter: requireRole(['Super Admin'], '/admin/distributors')
  },
  {
    path: '/distributors/:id',
    name: 'distributor_edit',
    component: DistributorAddEdit,
    beforeEnter: requireRole(['Super Admin'], '/admin/distributors')
  },
];

let campaignRoutes = [
  {
    path: '/campaigns',
    name: 'campaign_list',
    component: CampaignList,
  },
  {
    path: '/campaigns/add',
    name: 'campaign_add',
    component: CampaignAddEdit,
  },
  {
    path: '/campaigns/:id',
    name: 'campaign_edit',
    component: CampaignAddEdit,
  },
];

let vendorRoutes = [
  {
    path: '/vendors',
    name: 'vendor_list',
    component: VendorList,
  },
  {
    path: '/vendors/add',
    name: 'vendor_add',
    component: VendorAddEdit,
  },
  {
    path: '/vendors/:id',
    name: 'vendor_edit',
    component: VendorAddEdit,
  }
];

let orderRoutes = [
  {
    path: '/orders',
    name: 'order_list',
    component: OrderList,
  },
  {
    path: '/orders/:id',
    name: 'order_view',
    component: OrderView,
  }
];

// let reportRoutes = [
//   {
//     path: '/report',
//     name: 'report',
//     component: Report,
//   }
// ];

let productAttributeRoutes = [
  {
    path: '/product_attributes',
    name: 'product_attribute_list',
    component: ProductAttributeList,
  },
  {
    path: '/product_attributes/add',
    name: 'product_attribute_add',
    component: ProductAttributeAddEdit,
  },
  {
    path: '/product_attributes/:id',
    name: 'product_attribute_edit',
    component: ProductAttributeAddEdit,
  },
];

let productTypeRoutes = [
  {
    path: '/product_types',
    name: 'product_type_list',
    component: ProductTypeList,
  },
  {
    path: '/product_types/add',
    name: 'product_type_add',
    component: ProductTypeAddEdit,
  },
  {
    path: '/product_types/:id',
    name: 'product_type_edit',
    component: ProductTypeAddEdit,
  }
];

// let productVariantRoutes = [
//   {
//     path: '/product_variants/add/:id',
//     name: 'variantAdd',
//     component: VariantAdd,
//   },
//   {
//     path: '/product_variants/edit/:id',
//     name: 'variantEdit',
//     component: VariantEdit,
//   },
// ];

let productRoutes = [
  {
    path: '/products',
    name: 'product_list',
    component: ProductList,
  },
  {
    path: '/products/add',
    name: 'product_add',
    component: ProductAddEdit,
  },
  {
    path: '/products/:id',
    name: 'product_view',
    component: ProductView,
  },
  {
    path: '/products/edit/:id',
    name: 'product_edit',
    component: ProductAddEdit,
  }
];

let adminAreaOtherPages = [
  {
    path: '',
    name: 'home_page',
    component: TheHomePage,
  },
  // {
  //   path: '/edit_images/:id',
  //   name: 'editImages',
  //   component: EditImages,
  // },
  // {
  //   path: '/edit_images_variant/:id',
  //   name: 'editImagesVariant',
  //   component: EditImagesVariant,
  // },
  // {
  //   path: '/storefront_preview/:id',
  //   name: 'StorefrontPreview',
  //   component: StorefrontPreview,
  // },
];

let publicRoutes = [
  {
    path: '/login',
    name: 'login_page',
    component: TheLoginPage
  },
  // {
  //   path: '/',
  //   name: 'Storefront',
  //   component: Storefront,
  // },
  // {
  //   path: '/cart',
  //   name: 'Cart',
  //   component: Cart,
  // },
  // {
  //   path: '/order_confirmation',
  //   name: 'OrderConfirmation',
  //   component: OrderConfirmation
  // }
];

const router = new Router({
  routes: [
    ...withPrefix('', publicRoutes),

    ...withPrefix('/admin',
      [
        ...accountRoutes,
        ...distributorRoutes,
        ...campaignRoutes,
        ...vendorRoutes,
        ...orderRoutes,
        // ...reportRoutes,
        ...productAttributeRoutes,
        ...productTypeRoutes,
        // ...productVariantRoutes,
        ...productRoutes,
        ...adminAreaOtherPages,
      ]
    ),
    {path: '*', TheNotFoundPage}
  ],
  mode: 'history'
});

// check for user authentication before rendering the requested page
router.beforeEach(requireToken);

export default router;
