from setuptools import setup

package_name = 'a_team'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cshe97',
    maintainer_email='cshe97@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'Light = a_team.Light:main',
        'passiveLight = a_team.passiveLight:main',
        'pub_pt_msg = a_team.pub_pt_msg:main',
        'timer_test = a_team.timer_test:main',
        'green = a_team.test_green:main',

        'auto_driving = a_team.auto_driving:main',    
        ],
    },
)
