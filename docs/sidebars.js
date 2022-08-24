/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  //tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually

  aboutSidebar: [
    {
      type: "autogenerated",
      dirName: "about",
    },
  ],
  gettingstartedSidebar: [
    {
      type: "doc",
      id: "gettingstarted/start",
      label: "Introduction",
    },
    {
      type: "doc",
      id: "gettingstarted/ocplugin",
      label: "Installing the Owncloud plugin",
    },
    {
      type: "doc",
      id: "gettingstarted/kubernetes",
      label: "Configuring Kubernetes",
    },
    {
      type: "doc",
      id: "gettingstarted/zenodo",
      label: "Setting up Zenodo",
    },
    {
      type: "doc",
      id: "gettingstarted/updating",
      label: "Updating Sciebo RDS",
    },
  ],
  configurationSidebar: [
    {
      type: "doc",
      id: "documentation/configuration/index",
      label: "Configuration",
    },
    {
      type: "category",
      label: "Setting up your EFSS",
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: "doc",
          id: "documentation/configuration/efss/owncloud",
          label: "Owncloud",
        },
        {
          type: "doc",
          id: "documentation/configuration/efss/nextcloud",
          label: "Nextcloud",
        },
      ],
    },
    {
      type: "category",
      label: "Setting up services",
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: "doc",
          id: "documentation/configuration/services/zenodo",
          label: "Zenodo",
        },
        {
          type: "doc",
          id: "documentation/configuration/services/osf",
          label: "OSF",
        },
      ],
    },
    {
      type: "doc",
      id: "documentation/configuration/advanced-values-yaml",
      label: "Advanced values.yaml",
    },
  ],
  developmentSidebar: [
    {
      type: "doc",
      id: "documentation/development/index",
      label: "Development",
    },
    {
      type: "doc",
      id: "documentation/development/monorepo",
      label: "Monorepo Structure",
    },
    {
      type: "doc",
      id: "documentation/development/microservices",
      label: "Microservice architecture",
    },
    {
      type: "doc",
      id: "documentation/development/contributing/developing-connectors",
      label: "Developing Connectors",
    },
    {
      type: "doc",
      id: "documentation/development/contributing/developing-for-efss",
      label: "Developing a Plugin for your EFSS",
    },
    {
      type: "doc",
      id: "documentation/development/contributing/documentation",
      label: "Contributing to the Documentation",
    },
    {
      type: "category",
      label: "Kubernetes Layers",
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: "category",
          label: "Layer 1",
          collapsible: true,
          collapsed: true,
          items: [
            {
              type: "doc",
              id: "impl/layer1-port-invenio-docstring",
              label: "Port Invenio",
            },
            {
              type: "doc",
              id: "impl/layer1-port-osf-docstring",
              label: "Port OSF",
            },
            {
              type: "doc",
              id: "impl/layer1-port-owncloud-docstring",
              label: "Port Owncloud",
            },
          ],
        },
        {
          type: "category",
          label: "Layer 2",
          collapsible: true,
          collapsed: true,
          items: [
            {
              type: "doc",
              id: "impl/layer2-exporter-service-docstring",
              label: "Exporter Service",
            },
            {
              type: "doc",
              id: "impl/layer2-metadata-service-docstring",
              label: "Metadata Service",
            },
            {
              type: "doc",
              id: "impl/layer2-port-service-docstring",
              label: "Port Service",
            },
          ],
        },
        {
          type: "category",
          label: "Layer 3",
          collapsible: true,
          collapsed: true,
          items: [
            {
              type: "doc",
              id: "impl/layer3-research-manager-docstring",
              label: "Research Manager",
            },
            {
              type: "doc",
              id: "impl/layer3-token-storage-docstring",
              label: "Token Storage",
            },
          ],
        },
      ],
    },
  ],
  referenceSidebar: [
    {
      type: "doc",
      id: "documentation/reference/index",
      label: "Reference",
    },
    {
      type: "doc",
      id: "documentation/reference/environment-variables",
      label: "Environment Variables",
    },
    {
      type: "doc",
      id: "documentation/reference/glossary",
      label: "Glossary",
    },
    {
      type: "doc",
      id: "documentation/reference/arc42",
      label: "ARC42 Definition",
    },
  ],
};

module.exports = sidebars;
