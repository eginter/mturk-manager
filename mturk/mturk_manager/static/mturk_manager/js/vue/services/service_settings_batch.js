import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';

class Class_Settings_Batch {
  async loadPage(pagination) {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_settings_batch',
          'moduleProjects',
        ),
        project,
      },
      params: {
        page: pagination.page,
        page_size: pagination.rowsPerPage,
        sort_by: pagination.sortBy,
        descending: pagination.descending,
      },
    });

    store.commit('moduleSettingsBatch/setItems', {
      data: response.data.data,
      project,
    });

    return response.data.items_total;
  }

  async create({ settings_batch, project }) {
    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'url_api_projects_settings_batch',
          'moduleProjects',
        ),
        project,
      },
      data: settings_batch,
    });

    store.commit('moduleSettingsBatch/add', {
      data: response.data,
    });
  }

  async edit({ settings_batch_current, settings_batch_new, project }) {
    const data_changed = settings_batch_current.get_changes(settings_batch_new);

    if (Object.keys(data_changed).length === 0) return;

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url(
          'url_api_projects_settings_batch',
          'moduleProjects',
        ),
        value: settings_batch_current.id,
        project,
      },
      data: data_changed,
    });

    store.commit('moduleSettingsBatch/update', {
      data: response.data,
    });
  }

  async delete({ settings_batch, project, callback }) {
    const response = await Service_Endpoint.make_request({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          'url_api_projects_settings_batch',
          'moduleProjects',
        ),
        project,
        value: settings_batch.id,
      },
    });

    callback();
    store.commit('moduleSettingsBatch/delete', {
      settingsBatch: settings_batch,
    });
  }
}

export const ServiceSettingsBatch = new Class_Settings_Batch();
