import os

import gitlab


class GitLabTools:

    def __init__(self):
        self.gl = gitlab.Gitlab(os.environ['GITLAB_URL'], private_token=os.environ['GITLAB_PRIVATE_TOKEN'])

    def list_group_milestones(self):
        """
        List group milestones
        :return: group milestones
        """
        group_milestones = []
        groups = self.gl.groups.list()
        for group in groups:
            [
                group_milestones.append(
                    {
                        'milestone': milestone.__dict__['_attrs'],
                        'issues': [issue.__dict__['_attrs'] for issue in milestone.issues()]
                    }
                )
                for milestone in group.milestones.list(state='active')
            ]
        return group_milestones

    def list_project_milestones(self):
        """
        List project milestones
        :return: project milestones
        """
        project_milestones = []
        projects = self.gl.projects.list(all=True)
        for project in projects:
            for milestone in project.milestones.list(state='active'):
                # Remove project milestone has no start date or due date
                if (
                        milestone.__dict__['_attrs']['due_date'] is not None and
                        milestone.__dict__['_attrs']['start_date'] is not None
                ):
                    project_milestones.append(milestone.__dict__['_attrs'])
        [print(milestone) for milestone in project_milestones]
        return project_milestones
