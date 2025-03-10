import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { BaseLoadPageService } from './baseLoadPage.service';

class Class_Service_HITs extends BaseLoadPageService {
  async load_page(pagination, filters) {
    const useSandbox = store.state.module_app.use_sandbox;

    return Class_Service_HITs.loadPage({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'url_api_projects_hits',
          'moduleHITs',
        ),
        use_sandbox: useSandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      callback(response) {
        store.commit('moduleHITs/set_hits', {
          data: response.data.data,
          use_sandbox: useSandbox,
        });
      },
    });
  }
  // async set_hits({object_batches, data_batches, use_sandbox})
  // {
  //     store.commit('moduleHITs/set_hits', {
  //         object_batches,
  //         data_batches,
  //         use_sandbox
  //     });
  //
  //     await Service_Assignments.set_assignments({
  //         object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
  //         data_batches,
  //         use_sandbox
  //     });
  // }
  //
  // async append_hits({data_batches, use_sandbox})
  // {
  //      await Service_Assignments.append_assignments({
  //         data_batches,
  //         object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
  //         use_sandbox,
  //     });
  // }
}

export const Service_HITs = new Class_Service_HITs();
