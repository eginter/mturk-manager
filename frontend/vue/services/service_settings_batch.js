import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';
import Settings_Batch from '../classes/settings_batch';
import { BaseLoadPageService } from './baseLoadPage.service';

class Class_Settings_Batch extends BaseLoadPageService {
  async loadPage(pagination, filters) {
    const project = store.getters['moduleProjects/get_project_current'];

    return Class_Settings_Batch.loadPage({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
      },
      callback(response) {
        store.commit('moduleSettingsBatch/setItems', {
          data: response.data.data,
          project,
        });
      },
    });
  }

  async getAll() {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatchAll',
          'moduleSettingsBatch',
        ),
        project,
      },
      params: {
        fields: [
          'id',
          'name',
        ],
      },
    });

    return response.data;
  }

  async get(idSettingsBatch) {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        value: idSettingsBatch,
        project,
      },
    });

    return new Settings_Batch(response.data);
  }

  async create({ settings_batch, project }) {
    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
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
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
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
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
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
